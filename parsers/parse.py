import pip
pip.main(['install', 'PyPDF2'])
import os
import csv
import PyPDF2

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pathBills = os.path.join(base_dir, "BILLS")
pathItems = os.path.join(base_dir, "ITEMS")
done_file = os.path.join(base_dir, "LOGS", "done.txt")

files = os.listdir(pathBills)

done = []
if os.path.exists(done_file):
    with open(done_file, 'r', encoding='utf-8') as file:
        done = file.read().split('\n')

files = [f for f in files if f not in done and f.strip() and f != ".DS_Store"]

done += files
with open(done_file, 'w', encoding='utf-8') as file:
    file.write("\n".join(done))

def csv_to_nested_list(file_path):
    if not os.path.exists(file_path):
        return [["PARTY NAME", "DATE", "QUANTITY", "PRICE", "VALUE"]]
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        return list(csv.reader(csv_file))

def updating_csv(lst):
    for idx, i in enumerate(lst):
        if idx < 2:
            continue

        lst2 = [lst[0], lst[1]]
        itemDet = i.split(" ")
        if len(itemDet) < 5:
            continue

        quantity = itemDet[-1]
        if quantity in ["", "Pcs", "Set", "Pkt", "Dzn", "Pair", "Kit", "KIT"]:
            quantity = itemDet[-2]
            if quantity in ["", "Pcs", "Set", "Pkt", "Dzn", "Pair", "Kit", "KIT"]:
                quantity = itemDet[-3]
                price = itemDet[-4]
                value = itemDet[-5]
                if value in ["", "Pcs", "Set", "Pkt", "Dzn", "Pair", "Kit", "KIT"]:
                    value = itemDet[-6]
            else:
                price = itemDet[-3]
                value = itemDet[-4]
                if value in ["", "Pcs", "Set", "Pkt", "Dzn", "Pair", "Kit", "KIT"]:
                    value = itemDet[-5]
        else:
            price = itemDet[-1]
            value = itemDet[-3]
            if value in ["", "Pcs", "Set", "Pkt", "Dzn", "Pair", "Kit", "KIT"]:
                value = itemDet[-4]
            price = price.replace("Pcs", "").replace("Set", "").replace("Pkt", "").replace("Dzn", "").replace("Pair", "").replace("Kit", "").replace("KIT", "")
            if price.replace('.', '', 1).isdigit() and value.replace('.', '', 1).isdigit():
                quantity = str(int(float(value) / float(price)))

        price = price.replace("Pcs", "").replace("Set", "").replace("Pkt", "").replace("Dzn", "").replace("Pair", "").replace("Kit", "").replace("KIT", "")
        index_lst = itemDet.index(value)
        item_name = " ".join(itemDet[:index_lst]).replace("/", "|").strip()

        if len(item_name) < 5:
            continue

        lst2 += [quantity, price, value]
        item_csv_path = os.path.join(pathItems, item_name + ".csv")
        nested_lst = csv_to_nested_list(item_csv_path)
        nested_lst2 = []
        found = 0

        for row in nested_lst:
            if row[0].replace(" ", "").lower() == lst[0].replace(" ", "").lower():
                found = 1
                for j, l in enumerate(lst2[::-1]):
                    if j < 4:
                        row.insert(1, l)
            nested_lst2.append(row)

        if not found:
            nested_lst2.append(lst2)

        max_len = max(len(m) for m in nested_lst2)
        cols = (max_len - 1) // 4
        nested_lst2[0] = ["PARTY NAME"] + ["DATE", "QUANTITY", "PRICE", "VALUE"] * cols

        os.makedirs(os.path.dirname(item_csv_path), exist_ok=True)
        with open(item_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv.writer(csv_file).writerows(nested_lst2)

def getPDFContent(pdf_path):
    with open(pdf_path, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        billcontinue = 0
        partyName = ""

        for j in pdfReader.pages:
            pageList = j.extract_text().split('\n')
            found = 0
            lst = []

            for i in pageList:
                if "Dated" in i:
                    n = pageList.index(i)
                    lst.append(pageList[n + 1])
                if "DELHI" in i:
                    if billcontinue:
                        lst.append(partyName)
                    else:
                        n = pageList.index(i)
                        k = pageList[n + 1].replace("Invoice No.", "").strip()
                        partyName = k if k else "ON CASH"
                        lst.append(partyName)
                if "Rate Quantity" in i:
                    found = 1
                    continue
                if any(x in i for x in ["continued", "PACKING & FORWARDING", "Total", "GST", "FRIEGHT", "GREEN TAX"]):
                    billcontinue = 1 if "continued" in i else 0
                    found = 0
                    continue
                if found:
                    lst.append(i)

            updating_csv(lst)

for filename in files:
    getPDFContent(os.path.join(pathBills, filename))
