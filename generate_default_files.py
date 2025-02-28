default_data = {
    "default_apache.txt": """
index.html
index.php
server-status
.htaccess
robots.txt
wp-config.php
wp-admin/
cgi-bin/
logs/
backup/
uploads/
temp/
    """,
    "default_nginx.txt": """
index.html
index.php
nginx.conf
robots.txt
wp-config.php
wp-admin/
cgi-bin/
logs/
backup/
cached/
temp/
    """,
    "default_iis.txt": """
index.html
default.aspx
web.config
robots.txt
iisstart.htm
aspnet_client/
logs/
backup/
temp/
    """,
    "default_other.txt": """
index.html
index.php
default.conf
robots.txt
wp-config.php
wp-admin/
cgi-bin/
logs/
backup/
    """,
    "default_nginx_1_19_0.txt": """
index.html
index.php
nginx.conf
default.conf
robots.txt
wp-config.php
wp-admin/
cgi-bin/
logs/
backup/
cached/
temp/
debug.log
server-status
    """,
    "default_apache_2_4_62.txt": """
index.html
index.php
server-status
.htaccess
robots.txt
wp-config.php
wp-admin/
cgi-bin/
logs/
backup/
uploads/
temp/
debug.log
error_log
apache2.conf
default-ssl.conf
sites-available/
sites-enabled/
mods-available/
mods-enabled/
    """
}

def create_default_files():
    for filename, content in default_data.items():
        with open(filename, "w") as file:
            file.write(content.strip() + "\n")
        print(f"[+] Created: {filename}")

if __name__ == "__main__":
    create_default_files()
    print("\nAll default files have been created successfully.")

