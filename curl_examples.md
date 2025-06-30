# Business Analysis API - Curl Examples

## Base URL
```
http://localhost:8000/api/v1
```

## 1. Create a Coffee Shop Business

```bash
curl -X POST "http://localhost:8000/api/v1/business/create" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Brew & Bean Coffee Shop",
    "description": "A cozy coffee shop serving specialty coffee, pastries, and light meals in a warm, welcoming atmosphere",
    "business_type": "coffee_shop",
    "location": "Bangkok, Thailand",
    "target_market": "Young professionals, students, and coffee enthusiasts aged 20-45",
    "competitors": ["Starbucks", "Amazon Coffee", "Cafe Amazon", "True Coffee"],
    "growth_goals": ["Open 3 locations within 2 years", "Build strong brand recognition", "Achieve 20% monthly revenue growth"]
  }'
```

## 2. Create a Tech Startup Business

```bash
curl -X POST "http://localhost:8000/api/v1/business/create" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "DataFlow Analytics",
    "description": "AI-powered business intelligence platform that helps companies make data-driven decisions",
    "business_type": "tech_startup",
    "location": "Singapore",
    "target_market": "Medium to large enterprises in finance, retail, and healthcare sectors",
    "competitors": ["Tableau", "Power BI", "Looker", "Qlik"],
    "growth_goals": ["Reach 100 enterprise customers", "Achieve $5M ARR", "Expand to 3 new markets"]
  }'
```

## 3. Full Business Analysis for Restaurant

```bash
curl -X POST "http://localhost:8000/api/v1/business/process" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Spice Garden Thai Restaurant",
    "business_type": "restaurant",
    "location": "Bangkok, Thailand",
    "description": "Authentic Thai restaurant serving traditional dishes with modern presentation",
    "target_market": "Tourists, expats, and local families seeking authentic Thai cuisine",
    "competitors": ["Blue Elephant", "Nahm", "Issaya Siamese Club", "Gaggan"],
    "growth_goals": ["Open 2 more locations", "Launch delivery service", "Create catering business"],
    "initial_investment": 500000,
    "team_size": 15,
    "unique_value_proposition": "Authentic Thai flavors with modern dining experience",
    "business_model": "b2c",
    "industry": "food_beverage",
    "market_size": "local",
    "technology_requirements": ["POS system", "Online ordering", "Inventory management"],
    "regulatory_requirements": ["Food safety certification", "Business license", "Health permits"]
  }'
```

## 4. Create a Consulting Firm

```bash
curl -X POST "http://localhost:8000/api/v1/business/create" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Strategic Solutions Consulting",
    "description": "Management consulting firm specializing in digital transformation and business strategy",
    "business_type": "consulting_firm",
    "location": "Bangkok, Thailand",
    "target_market": "Mid-size companies looking to digitize and scale their operations",
    "competitors": ["McKinsey", "BCG", "Bain", "Deloitte"],
    "growth_goals": ["Serve 50 clients annually", "Expand to regional markets", "Build thought leadership"]
  }'
```

## 5. Create a Retail Store

```bash
curl -X POST "http://localhost:8000/api/v1/business/create" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "EcoStyle Fashion Boutique",
    "description": "Sustainable fashion boutique offering eco-friendly clothing and accessories",
    "business_type": "retail_store",
    "location": "Chiang Mai, Thailand",
    "target_market": "Environmentally conscious consumers aged 25-40",
    "competitors": ["H&M Conscious", "Zara Join Life", "Patagonia", "Local boutiques"],
    "growth_goals": ["Open online store", "Launch sustainable fashion line", "Partner with local artisans"]
  }'
```

## 6. Create an E-commerce Business

```bash
curl -X POST "http://localhost:8000/api/v1/business/process" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "ThaiCraft Marketplace",
    "business_type": "ecommerce",
    "location": "Bangkok, Thailand",
    "description": "Online marketplace connecting local Thai artisans with global customers",
    "target_market": "International customers interested in authentic Thai handicrafts",
    "competitors": ["Etsy", "Amazon Handmade", "Local craft markets"],
    "growth_goals": ["Onboard 500 artisans", "Reach 10,000 customers", "Expand to 5 countries"],
    "initial_investment": 200000,
    "team_size": 8,
    "unique_value_proposition": "Authentic Thai handicrafts with fair trade practices",
    "business_model": "marketplace",
    "industry": "retail",
    "market_size": "international",
    "technology_requirements": ["E-commerce platform", "Payment gateway", "Inventory management"],
    "regulatory_requirements": ["Business registration", "Tax compliance", "Export permits"]
  }'
```

## 7. Get All Businesses

```bash
curl -X GET "http://localhost:8000/api/v1/business/?limit=10"
```

## 8. Get Specific Business (replace {business_id})

```bash
curl -X GET "http://localhost:8000/api/v1/business/{business_id}"
```

## 9. Get Business Analysis (replace {business_id})

```bash
curl -X GET "http://localhost:8000/api/v1/business/{business_id}/analysis"
```

## 10. Search Businesses

```bash
# Search by name/description
curl -X GET "http://localhost:8000/api/v1/business/search?q=coffee"

# Search with business type filter
curl -X GET "http://localhost:8000/api/v1/business/search?q=restaurant&business_type=restaurant"
```

## 11. Delete Business (replace {business_id})

```bash
curl -X DELETE "http://localhost:8000/api/v1/business/{business_id}"
```

## 12. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## 13. Root Endpoint

```bash
curl -X GET "http://localhost:8000/"
```

## 14. API Documentation

```bash
# Swagger UI
curl -X GET "http://localhost:8000/docs"

# ReDoc
curl -X GET "http://localhost:8000/redoc"
```

## Business Types Available

- `coffee_shop`
- `restaurant`
- `tech_startup`
- `consulting_firm`
- `retail_store`
- `ecommerce`
- `manufacturing`
- `healthcare`
- `education`
- `real_estate`
- `finance`
- `tourism`
- `agriculture`
- `logistics`
- `marketing`

## Industry Types Available

- `food_beverage`
- `technology`
- `retail`
- `services`
- `healthcare`
- `education`
- `finance`
- `manufacturing`
- `tourism`
- `agriculture`
- `real_estate`
- `logistics`
- `marketing`
- `consulting`

## Business Models Available

- `b2c` (Business to Consumer)
- `b2b` (Business to Business)
- `marketplace`
- `subscription`
- `franchise`
- `direct_sales`
- `wholesale`
- `dropshipping`
- `saas` (Software as a Service)
- `agency`

## Market Sizes Available

- `local`
- `regional`
- `national`
- `international`
- `global` 