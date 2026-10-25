from mcp.server.fastmcp import FastMCP

mcp=FastMCP("bmi server")

@mcp.tool()
def calculate_bmi(weight_kg:float,height_m:float)->float:
    """Calculate BMI given weight in kilograms and height in meters."""
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    bmi = weight_kg / (height_m ** 2)
    return bmi

if __name__ == "__main__":
    mcp.run(transport="stdio")