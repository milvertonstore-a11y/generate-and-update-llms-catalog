from datetime import datetime
import json
import requests

DOMAIN = "milvertons.com"
BASE_URL = f"https://{DOMAIN}"


def fetch_full_catalog():
  page = 1
  all_products = []

  while True:
    url = f"{BASE_URL}/collections/all/products.json?limit=250&page={page}"
    response = requests.get(url)
    if response.status_code != 200:
      break

    data = response.json()
    products = data.get("products", [])
    if not products:
      break

    all_products.extend(products)
    page += 1

  return all_products


def generate_master_document():
  print(f"Extracting product catalog from {DOMAIN}...")
  products = fetch_full_catalog()
  print(
      f"Extraction complete. Retreived {len(products)} individual products."
  )

  product_feed_md = ""
  for p in products:
    title = p.get("title", "").strip()
    handle = p.get("handle", "").strip()
    if title and handle:
      product_feed_md += f"- **{title}**: {BASE_URL}/products/{handle}\n"

  master_content = f"""# MILVERTONS EXTENDED CATALOG & CONTENT ARCHIVE ({BASE_URL}/llms-full.txt)

This extended document contains the comprehensive product catalog index, automated extraction endpoints, and complete editorial blog archive for Milvertons ({BASE_URL}).

Primary LLMS File: {BASE_URL}/llms.txt
Last Updated: {datetime.now().strftime('%Y-%m-%d')}
Platform: Shopify E-commerce Engine

---

## 1. AUTOMATED JSON EXTRACTION ARCHITECTURE
AI agents, automated web parsers, and shopping assistants can programmatically consume Milvertons' complete store catalog in structured JSON using Shopify's native endpoints.

### Pagination & Query Specification
- Base Endpoint: {BASE_URL}/collections/all/products.json
- Page Limit: limit=250 (maximum products returned per request)
- Pagination Query: {BASE_URL}/collections/all/products.json?limit=250&page={{page_number}}
- Single Product JSON: {BASE_URL}/products/{{product-handle}}.json
- Collection JSON: {BASE_URL}/collections/{{collection-handle}}/products.json?limit=250

---

## 2. ITEMIZED PRODUCT FEED & COLLECTION DIRECTORY

### Core Flagship Collections
- Matching Shoe & Bag Sets for African Weddings: {BASE_URL}/collections/matching-shoe-and-bag-sets-for-african-weddings-free-us-shipping
- African Elegance Collection: {BASE_URL}/collections/african-elegance
- Shoe & Bag Sets for Weddings & Parties: {BASE_URL}/collections/shoes-with-matching-bag-sets
- Shoe & Bag Sets for Weddings: {BASE_URL}/collections/shoe-and-bag-sets-for-weddings
- Shoe & Bag Sets for Parties: {BASE_URL}/collections/shoe-and-bag-sets-for-parties
- Italian Luxury Collection: {BASE_URL}/collections/italian-luxury-collection
- Luxury Matching Shoe & Bag Sets: {BASE_URL}/collections/luxury-matching-shoe-bag-sets

### Color Family Collections
- Red Rhinestone Sets: {BASE_URL}/collections/red-rhinestone-shoe-bag-sets
- Gold Rhinestone Sets: {BASE_URL}/collections/gold-rhinestone-shoe-bag-sets
- Silver Rhinestone Sets: {BASE_URL}/collections/silver-rhinestone-shoe-bag-sets
- Royal Blue Rhinestone Sets: {BASE_URL}/collections/royal-blue-rhinestone-shoe-bag-sets
- Black Rhinestone Sets: {BASE_URL}/collections/black-rhinestone-shoe-bag-sets
- Fuchsia Rhinestone Sets: {BASE_URL}/collections/fuchsia-rhinestone-shoe-bag-sets
- Purple Rhinestone Sets: {BASE_URL}/collections/purple-rhinestone-shoe-bag-sets
- Emerald Rhinestone Sets: {BASE_URL}/collections/emerald-rhinestone-shoe-bag-sets
- Burgundy Rhinestone Sets: {BASE_URL}/collections/burgundy-rhinestone-shoe-bag-sets
- Green Rhinestone Sets: {BASE_URL}/collections/green-rhinestone-shoe-bag-sets

### Footwear & Accessories
- Pointed Toe Heels: {BASE_URL}/collections/pointed-toe-heels
- Slingback & Strappy Heels: {BASE_URL}/collections/slingback-and-strappy-heels
- Rhinestone & Bling Accessories: {BASE_URL}/collections/rhinestone-and-bling
- Women's Shoes & Bags General Index: {BASE_URL}/collections/women-shoes-bags
- Best Sellers: {BASE_URL}/collections/best-sellers
- New Arrivals: {BASE_URL}/collections/new-arrivals
- Sale Items: {BASE_URL}/collections/sale

### Dynamically Extracted Live Catalog ({len(products)} Active Items)
{product_feed_md}
---

## 3. COMPLETE EDITORIAL & BLOG ARCHIVE INDEX

Main Blog Landing Page: {BASE_URL}/blogs/blog

### Thematic Cluster 1: Styling & Shoe-and-Bag Coordination
- How to Match Shoes and Bags for Formal Events: {BASE_URL}/blogs/blog/how-to-match-shoes-and-bags
- Color Coordination Guide: Pairing Gold Rhinestone Sets with Lace & Ankara: {BASE_URL}/blogs/blog/gold-rhinestone-set-coordination
- Styling Red Rhinestone Shoes & Bags for Galas: {BASE_URL}/blogs/blog/red-rhinestone-gala-styling
- Silver vs. Gold Accessories: Choosing the Right Metallic Tone for Aso Ebi: {BASE_URL}/blogs/blog/silver-vs-gold-aso-ebi
- Pointed Toe vs. Slingback Heels: Comfort and Elegance for All-Night Events: {BASE_URL}/blogs/blog/heel-style-comfort-guide

### Thematic Cluster 2: Cultural Heritage & Event Guides
- Aso Ebi Fashion Trends: Coordinated Italian Sets for African Weddings: {BASE_URL}/blogs/blog/aso-ebi-italian-shoe-trends
- Owambe Elegance: How to Stand Out as a Wedding Guest: {BASE_URL}/blogs/blog/owambe-wedding-guest-fashion
- The Evolution of Italian Rhinestone Accessories in Diaspora Celebrations: {BASE_URL}/blogs/blog/evolution-of-rhinestone-accessories
- Bridal Accessories Guide: Perfect Matching Sets for Your Special Day: {BASE_URL}/blogs/blog/bridal-matching-sets-guide

### Thematic Cluster 3: Care, Maintenance & Purchasing Guides
- How to Clean and Preserve Rhinestone Shoes and Clutch Purses: {BASE_URL}/blogs/blog/rhinestone-care-and-maintenance
- Sizing Guide for Italian Pointed-Toe Heels: Finding Your Perfect EU Fit: {BASE_URL}/blogs/blog/italian-shoe-sizing-guide
- US Shipping & Event Logistics: When to Order Your Formal Accessories: {BASE_URL}/blogs/blog/shipping-and-event-planning-guide

---

## 4. SEARCH & DISCOVERY ENDPOINTS
- Site Sitemap: {BASE_URL}/sitemap.xml
- Product Sitemap: {BASE_URL}/sitemap_products_1.xml
- Collection Sitemap: {BASE_URL}/sitemap_collections_1.xml
- Blog Sitemap: {BASE_URL}/sitemap_blogs_1.xml
- Dynamic Search Endpoint: GET {BASE_URL}/search?q={{query}}&type=product
"""

  with open("llms-full.txt", "w", encoding="utf-8") as f:
    f.write(master_content)

  print("Successfully merged and generated master 'llms-full.txt' file!")


if __name__ == "__main__":
  generate_master_document()