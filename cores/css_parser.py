def parssing_css(theme_name) -> dict:

    content = []
    try:
        # [+] Reading The CSS file
        with open(theme_name, "r") as css_file:
            content = css_file.readlines()
    except Exception as error:
        print(f"[-] Error message: \n{error}")

    # [+] Data cleaning
    separator = "/*###################### I'm separator :) ######################*/"
    css_data = [line.strip() for line in content]
    temp = ""
    final_css = []
    for word in css_data:
        if word != separator:
            temp += word
        else:
            final_css.append(temp)
            temp = ""
    # [+] Final data
    parsed_data = {
            "mainQt": final_css[0],
            "tabWidget": final_css[1],

            # [+] Accounts tabe
            "accountsList": final_css[2],
            "editQRColor": final_css[3],
            "editQRButton": final_css[4],
            "editCopyButton": final_css[5],

            # [+] Edit Accounts tabe
            # Select/Add/Update buttons :)
            "editInputFields": final_css[6],
            "editManubuttons": final_css[7],
            "editShowButton": final_css[8],
            "editDeleteButton": final_css[9],
            "editLabels": final_css[10],
            "ediGroup": final_css[11],
            "editAccountsList_2": final_css[12],
            
            # [+] settings tabe
            "editHeaders": final_css[13],
            "editNormalLabels": final_css[14],
            "editSecFields": final_css[15],
            "editSecButtons": final_css[16],
    }
    return parsed_data
