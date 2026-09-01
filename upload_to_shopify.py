import os
import sys
import requests

ACCESS_TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
RAW_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "")

# Clean domain to remove protocols and trailing slashes
SHOP_DOMAIN = (
    RAW_DOMAIN.replace("https://", "").replace("http://", "").strip("/")
)
GRAPHQL_URL = f"https://{SHOP_DOMAIN}/admin/api/2026-01/graphql.json"

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN,
}


def staged_upload_create():
  """Step 1: Get a temporary S3/GCS upload target from Shopify."""
  query = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters {
            name
            value
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
  variables = {
      "input": [{
          "filename": "llms-full.txt",
          "mimeType": "text/plain",
          "httpMethod": "POST",
          "resource": "FILE",
      }]
  }

  res = requests.post(
      GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS
  )
  data = res.json()

  if "errors" in data or data.get("data", {}).get("stagedUploadsCreate", {}).get(
      "userErrors"
  ):
    print("Failed to get staged upload target:", data)
    sys.exit(1)

  target = data["data"]["stagedUploadsCreate"]["stagedTargets"][0]
  return target["url"], target["resourceUrl"], target["parameters"]


def upload_to_staged_target(upload_url, parameters, file_path="llms-full.txt"):
  """Step 2: POST the raw file to the staged URL."""
  form_data = {param["name"]: param["value"] for param in parameters}

  with open(file_path, "rb") as f:
    files = {"file": f}
    res = requests.post(upload_url, data=form_data, files=files)
    res.raise_for_status()


def file_create(resource_url):
  """Step 3: Register the uploaded file into Shopify Content > Files."""
  query = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          id
          createdAt
          ... on GenericFile {
            url
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
  variables = {
      "files": [
          {"originalSource": resource_url, "contentType": "FILE", "alt": "llms-full.txt extended catalog"}
      ]
  }

  res = requests.post(
      GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS
  )
  return res.json()


if __name__ == "__main__":
  if not ACCESS_TOKEN:
    print("Error: SHOPIFY_ADMIN_ACCESS_TOKEN is missing.")
    sys.exit(1)

  print("1. Requesting staged upload URL from Shopify GraphQL API...")
  upload_url, resource_url, parameters = staged_upload_create()

  print("2. Uploading llms-full.txt to Shopify staging storage...")
  upload_to_staged_target(upload_url, parameters)

  print("3. Registering file in Shopify Content > Files...")
  result = file_create(resource_url)
  print("Upload completed successfully!")
