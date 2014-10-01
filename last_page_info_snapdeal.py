import req_proxy
from bs4 import BeautifulSoup
from lxml import html 
import re 
import time 
import sys
import ast 



special_char = ['-', '! ', ' " ', '# ', '$ ', '%', '& ', "'", '(', ')', '* ', '+', ', ',  '. ', '/ ', ':', '; ', '<', '=', '> ', '? ', '@ ', '[', '\\ ', '] ', '^ ', '_ ', '` ', '{ ', '| ', '} ', '~ ', '\xc2\xb4 ', '#! ', '/* ', '*/ ', '&amp;', '']

special_char = map(str.strip, special_char)



def my_strip(x):
    try:
        x = str(x).strip()
    except:
        x = str(x.encode("ascii", "ignore")).strip()
    return x

       
def main(f2, line):    
    line_split = ast.literal_eval(line.strip())
    link = line_split[1]

    page = req_proxy.main(link)
    soup = BeautifulSoup(page, "html.parser")

    link_split = filter(None, link.split("/"))
    
    try:
        sku = soup.find("span", attrs={"id":"hightLightSupc"}).get_text()

    except:
        sku = link_split[-1]

    pro_title = link_split[-2]

    tar_sub_cat_box  = soup.find("div", attrs={"id":"breadCrumbWrapper"})
    tar_sub_cat_box2 = tar_sub_cat_box.find_all("div", attrs={"class":"containerBreadcrumb"})

    target_link = line_split[0]

    target1 = tar_sub_cat_box2[0].a.span.get_text().lower()
    target2 = tar_sub_cat_box2[0].a.span.get_text().lower()

    if "women" in target1 or  "women" in target2: 
        target = "women"
    elif "men" in target1 or  "men" in target2:
        target = "men"
    elif "unisex" in target1 or  "unisex" in target2:
        target = "unisex"
    elif "boy" in target1 or  "boy" in target2:
        target = "boy"
    elif "girl" in target1 or  "girl" in target2:
        target = "girl"
    elif "kid" in target1 or  "kid" in target2:
        target = "kid"
    elif "home" in target1 or  "home" in target2:
        target = "home & decor"
    elif "mobile" in target1 or  "mobile" in target2:
        target = "mobile"
    elif "appliance" in target1 or  "appliance" in target2:
        target = "appliance"
    elif "computer" in target1 or  "computer" in target2:
        target = "computer"
    elif "book" in target1 or  "book" in target2:
        target = "book"
    else:
         target = target1


    if len(tar_sub_cat_box2) == 3:
        cate = tar_sub_cat_box2[1].a.span.get_text()
        catelink = tar_sub_cat_box2[1].a.get("href")
        sub_cate = cate
        sub_cate_link = catelink
        ss__cate = cate
        ss__cate_link = catelink

    elif len(tar_sub_cat_box2) == 4:
        cate = tar_sub_cat_box2[1].a.span.get_text()
        catelink = tar_sub_cat_box2[1].a.get("href")
        sub_cate = tar_sub_cat_box2[2].a.span.get_text()
        sub_cate_link = tar_sub_cat_box2[2].a.get("href")
        ss__cate = sub_cate
        ss__cate_link =  sub_cate_link

    elif len(tar_sub_cat_box2) == 5:
        cate = tar_sub_cat_box2[1].a.span.get_text()
        catelink = tar_sub_cat_box2[1].a.get("href")
        sub_cate = tar_sub_cat_box2[2].a.span.get_text()
        sub_cate_link = tar_sub_cat_box2[2].a.get("href")
        ss__cate = tar_sub_cat_box2[3].a.span.get_text()
        ss__cate_link = tar_sub_cat_box2[3].a.get("href")


    else:
        cate = tar_sub_cat_box2[1].a.span.get_text()
        catelink = tar_sub_cat_box2[1].a.get("href")
        sub_cate = cate
        sub_cate_link = catelink
        ss__cate = cate
        ss__cate_link = catelink




    #brand_colour_tag = soup.find("div", attrs={"class":"personaliseWidgetWrapper pad_10_top"}).find_all("a")

    brand = line_split[0][line_split[0].rfind(":")+1:]

    try:
        colour = soup.find("li", text= re.compile("Color")).get_text()
        colour = colour[colour.rfind(":")+1:]
    except:
        colour = ''
    
        
    price_big_box = soup.find("div", attrs={"class":"priceandofferbox"})

    sp = ''

    try:
        sp = price_big_box.find("span", attrs={"id":"selling-price-id"}).get_text()
    except:
        pass

    try:
        mrp = price_big_box.find("span", attrs={"id":"original-price-id"}).get_text()

    except:
        mrp = sp


    start = sp.find(".")

    if start != -1:
        sp = "".join(sp.split(".")[-1].replace(",", "").split())

    else:
        sp = "".join(sp.split()[-1].replace(",", "").split())


    start = mrp.find(".")

    if start != -1:
        mrp = "".join(mrp.split(".")[-1].replace(",", "").split())

    else:
        mrp = "".join(mrp.split()[-1].replace(",", "").split())


    
    
    pro_image1 = soup.find("meta", attrs={"property":"og:image"}).get("content")    

    try:
        pro_image = soup.find("img", attrs={"class":"jqzoom zoomPad"}).get("src")
    except:
        pro_image = ''


    if not pro_image:
        pro_image = pro_image1


    pro_url = link 

    try:
        seller = soup.find("span", attrs={"id":"vendorName"}).get_text()
    
    except:
        seller = ''

    meta_title = soup.find("meta", attrs={"property":"og:title"}).get("content")
    meta_disc = soup.find("meta", attrs={"name":"description"}).get("content")

    try:
        desc = soup.find("div", attrs={"class":"detailssubbox"}).get_text()
    except:
        desc = ' '
    try:
        spec = soup.find("div", attrs={"class":"personaliseWidgetWrapper pad_10_top"}).get_text()
    except:
        spec = ' '

    dte = time.strftime("%d:%y:%Y")

    size = line_split[-1]
    status = soup.find("a", attrs={"id":"BuyButton-1"})

    if status:
        status = "A"

    else:
        status = "IA"


    start =   pro_image.rfind("/")
    sort_image_link = pro_image[start+1:]

    cate = cate.lower() 
    sub_cate = sub_cate.lower()
    ss__cate = ss__cate.lower()

    prl = "-".join("".join([c for c in pro_title if c not in special_char]).split()).lower()       


    desc , spec = tuple(map(my_strip, [desc, spec]))

    desc = "  ".join(desc.split())
    spec = "  ".join(spec.split())
    #desc = "".join(BeautifulSoup(desc, "html.parser").get_text().replace(">" ,",").split())
    #spec ="".join(BeautifulSoup(spec, "html.parser").get_text().replace(">" ,",").split())
    info = [sku, pro_title, prl, target_link, sp, cate, sub_cate, ss__cate, ss__cate_link, brand,
            pro_image, sort_image_link, mrp, colour, target,  pro_url, seller, meta_title, meta_disc, 
            str(size), desc, spec, dte, status]


    info2 = map(my_strip, info)

    f2.write(str(info2) + "\n")

   



def supermain():
    f2 = open("last_info.csv", "w+")
    #link = "http://www.snapdeal.com/product/samsung-galaxy-mega-gt-i9152/1412740"
    #link = "http://www.snapdeal.com/product/phoenix-black-gray-combo-of/1238671312"
    #link = "http://www.snapdeal.com/product/rts-whiteblack-sport-shoes/1072665786"
    #link = "http://www.snapdeal.com/product/samsung-galaxy-mega-gt-i9152/1412740"
    #link  = "http://www.snapdeal.com/product/real-red-black-blue-sneakers/1185686314"
    #link = "http://www.snapdeal.com/product/nivia-orange-football-shoes-football/804817762"
    #link = "http://www.snapdeal.com/product/silver-streak-pack-of-smart/1858917340"
    #link = "http://www.snapdeal.com/product/kbzeb-ps2-multimedia-keyboard-usb/1620795338"
    #link = "http://www.snapdeal.com/product/micromax-32b200-32-inches-hd/417760978"
    #link = "http://www.snapdeal.com/product/funai-32fe502-32-inches-slim/1388621"
    #link = "http://www.snapdeal.com/product/samsung-32eh4003-32-inches-hd/228527"

    #link = "http://www.snapdeal.com/product/puma-purple-poly-cotton-sleeveless/1570224367"
    line = "['http://www.snapdeal.com/products/home-kitchen-home-decoratives/?q=Brand:oocc', 'http://www.snapdeal.com/product/oocc-purple-floral-mirrored-base/1174355565', '[]']"
    main(f2, line)
    f2.close()


if __name__=="__main__":
    supermain()
    
