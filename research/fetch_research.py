import requests
import os

def download_pdf(url, filename):
    """
    Downloads a PDF from a URL and saves it to the research directory.
    """
    research_dir = os.path.dirname(__file__)
    file_path = os.path.join(research_dir, filename)
    
    if os.path.exists(file_path):
        print(f"Skipping: {filename} already exists.")
        return

    print(f"Downloading: {filename}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Success: Saved to {file_path}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    # High-value research papers discovered via search
    research_papers = [
        {
            "url": "https://www.icrisat.org/documents/document.291.aspx.pdf",
            "name": "CGIAR_2030_Strategy_Resilient_Drylands.pdf"
        },
        {
            "url": "https://www.unccd.int/sites/default/files/2022-06/SADC%20Drought%20Risk%20Management%20and%20Mitigation%20Strategy%20%282022-2032%29%20Vol%203.pdf",
            "name": "SADC_Drought_Strategy_Vol3.pdf"
        },
        {
            "url": "http://www.capri.cgiar.org/pdf/capriwp23.pdf",
            "name": "Drought_Risk_Management_WANA.pdf"
        }
    ]

    print("--- DroughtSense Research Downloader ---")
    for paper in research_papers:
        download_pdf(paper['url'], paper['name'])
    print("--- Download Task Complete ---")
