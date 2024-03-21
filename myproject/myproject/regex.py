import re

raw_text = '''
<div>
    <span class="actionBar__text"> Showing 18 of 101 products. </span>
</div>
'''

match = re.search(r'of (\d+) products', raw_text)
total_number = int(match.group(1)) if match else None
print(total_number)

