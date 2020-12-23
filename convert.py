""""Convert guid list into generic url list"""

with open("guids") as f:
    guids_1 = f.readlines()

guids = [x.replace('\n', '') for x in guids_1]

url_buffer = ""

for guid in guids:
    url_buffer += (f"https://image.halocdn.com/h5/requisition-packs/{guid}?locale=en&isGiftOnly=False&isAGift"
                   f"=False&flair=0&hash=jUEWSdFdFrQzlu44OlHYHxSmzee%2barhHEMHBCK%2fpRm0%3d\n")
    
with open("urls", "w") as f:
    f.write(url_buffer)
