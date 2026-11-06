from utils.stock_research import research_stock

result = research_stock("PLUG")

print("\nSTOCK RESEARCH RESULTS")

for key, value in result.items():
    print(f"{key}: {value}")