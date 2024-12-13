from bs4 import BeautifulSoup as bS
import requests as req

def decode_sec(url):
    # http request
    response = req.get(url)
    del url

    if response.status_code == 200:
        soup = bS(response.text, 'html.parser')
        content = soup.get_text(separator='\n')
        content = content.strip()
        del response

        # Extract content after heading
        extract = False
        extracted_content = ""
        for line in content.splitlines():
            if extract:
                extracted_content += line + "\n"
            if line.strip() == "y-coordinate":
                extract = True
        
        content = extracted_content
        del extracted_content, extract

        # Split content into individual rows
        lines = content.split("\n")
        grid_data = []
        for i in range(0, len(lines), 3):
            grid_data.append(lines[i:i+3])

        content = grid_data
        del grid_data

        # Grid dimensions
        max_x, max_y = 0, 0
        for row in content:
            if len(row) != 3:
                continue
            x_coord = int(row[0])
            y_coord = int(row[2])
            if x_coord > max_x:
                max_x = x_coord
            if y_coord > max_y:
                max_y = y_coord

        max_x, max_y = max_x + 1, max_y + 1
        grid = [[" " for _ in range(max_x)] for _ in range(max_y)]
        del max_x, max_y

        # Populate grid w/characters
        for row in content:
            if len(row) != 3:
                continue
            x_coord = int(row[0])
            char = row[1]
            y_coord = int(row[2])
            grid[y_coord][x_coord] = char
        del content, x_coord, y_coord

        # Print grid
        for row in grid:
            print("".join(row))
        del grid

url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
decode_sec(url)