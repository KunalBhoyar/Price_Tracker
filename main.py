from fastapi import FastAPI, Query
import scraper

app = FastAPI()

@app.get("/compare-price")
async def compare_price(product_name: str):
    ebay_price = scraper.scrape_ebay(product_name)
    flipkart_price = scraper.scrape_flipkart(product_name)
    amazon_uk_price = scraper.scrape_amazon_uk(product_name)
    return {
        "product": product_name,
        "prices": {
            "eBay": ebay_price,
            "Flipkart": flipkart_price,
            "Amazon UK": amazon_uk_price
        }
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    