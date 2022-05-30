

def parssing_css(theme_name) -> dict:

    # [+] Reading The CSS file
    content = []
    try:
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
            "self"                          : final_css[0],
            "tabWidget"                     : final_css[1],
            "listWidget"                    : final_css[2],
            "display_qr_btn"                : final_css[3],
            "decrypt_and_copy_password"     : final_css[4],
            "getting_account_id"            : final_css[5],
            "select_by_id"                  : final_css[6],
            "listWidget_edit_accounts"      : final_css[7],
            "edit_account_platform"         : final_css[8],
            "edit_account_email"            : final_css[9],
            "edit_account_password"         : final_css[10],
            "show_password"                 : final_css[11],
            "insert_account_data"           : final_css[12],
            "update_account_data"           : final_css[13],
            "delete_account_data"           : final_css[14]
        }
    return parsed_data
