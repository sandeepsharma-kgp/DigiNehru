
now="$(date +'%Y-%m-%d')"
yesterday="$(date --date="yesterday" +'%Y-%m-%d')"
file_name="$now.sql"
delete_file="$yesterday.sql"
rm -rf /tmp/$delete_file
mysqldump -u root -pdigitalnehru DigiNehru > ~/Dump/$file_name
