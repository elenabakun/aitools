import csv
import random
import urllib.parse

# Read the services.csv file
services = []
with open('services.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    services = list(reader)

# Shuffle the services randomly
random.shuffle(services)

# Generate HTML code
html = '''
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400" rel="stylesheet">
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f1f1f1;
        }
        .tag-cloud {
            max-width: 800px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
        .tag {
            display: inline-block;
            margin: 5px;
            padding: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Roboto', sans-serif;
            color: #fff;
            position: relative;
            transition: transform 0.3s ease;
            text-decoration: none;
        }
        .tag:hover {
            transform: scale(1.1);
        }
        .tag a {
            color: inherit;
            text-decoration: none;
        }
        .light-color {
            color: #000;
        }
        .tag:hover .balloon {
            display: block;
        }
        .balloon {
            display: none;
            position: absolute;
            padding: 10px;
            background-color: rgba(0, 0, 0, 1);
            color: #fff;
            border-radius: 5px;
            z-index: 1;
            font-size: 14px;
            font-weight: 300;
            width: 240px;
            text-align: center;
            line-height: 1.4;
            bottom: calc(100% + 10px);
            left: 50%;
            transform: translateX(-50%);
        }
        .description-block {
            margin-top: 20px;
            width: 800px;
            min-height: 200px;
            max-height: 400px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            text-align: center;
            font-family: 'Roboto', sans-serif;
            overflow-y: auto;
        }
    </style>
</head>
<body>
<div class="tag-cloud">
'''

# Generate tag cloud
for service in services:
    name = service[0]
    category = service[1]
    color = service[2]
    description = service[3]
    font_size = random.randint(12, 24)  # Random font size between 12 and 24 pixels

    # Remove whitespace characters and '#' symbol from color if present
    color = color.strip().lstrip('#')

    # Determine text color based on background color brightness
    brightness = (int(color[0:2], 16) * 299 + int(color[2:4], 16) * 587 + int(color[4:6], 16) * 114) / 1000
    text_color_class = 'light-color' if brightness > 127 else ''

    # Convert service name to URL format
    url_name = urllib.parse.quote(name)

    # Create a div for the tag with random font size and color
    html += f'<div class="tag {text_color_class}" style="font-size: {font_size}px; background-color: #{color};" onclick="searchBing(\'{url_name}\')">{name}'
    html += f'<div class="balloon"><span style="font-size: 16px; font-weight: bold;">{category}</span><br><br>{description}</div></div>'

html += '''
</div>
<div class="description-block"></div>
<script>
    function displaySearchResults(results) {
        const { value } = results.webPages;
        const searchResultsContainer = document.querySelector('.description-block');
        searchResultsContainer.innerHTML = '';

        value.forEach((result) => {
            const { name, url, snippet } = result;
            const resultElement = document.createElement('div');
            resultElement.className = 'search-result';

            const titleElement = document.createElement('h3');
            const linkElement = document.createElement('a');
            linkElement.href = url;
            linkElement.target = '_blank';
            linkElement.textContent = name;
            titleElement.appendChild(linkElement);

            const snippetElement = document.createElement('p');
            snippetElement.textContent = snippet;

            resultElement.appendChild(titleElement);
            resultElement.appendChild(snippetElement);

            searchResultsContainer.appendChild(resultElement);
        });
    }

    function searchBing(term) {
        // Replace 'YOUR-SUBSCRIPTION-KEY' with your own Bing Search API subscription key
        const subscriptionKey = '6906a2419e54496cb939189166c061b7';
        const url = `https://api.bing.microsoft.com/v7.0/search?q=${encodeURIComponent(term)}+AI+tool`;

        fetch(url, {
            headers: {
                'Ocp-Apim-Subscription-Key': subscriptionKey,
            },
        })
        .then((response) => response.json())
        .then((data) => {
            const webPages = data.webPages;
            if (webPages && webPages.value && webPages.value.length > 0) {
                displaySearchResults(data);
            } else {
                console.log('No search results found.');
            }
        })
        .catch((error) => {
            console.log('Error fetching search results:', error);
        });
    }
</script>

</body>
</html>
'''

# Rewrite the HTML file
with open('docs/index.html', 'w') as file:
    file.write(html)
