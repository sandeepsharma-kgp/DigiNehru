
now="$(date +'%Y-%m-%d')"
file_name="$now.sql"
mysqldump -u root -pdigitalnehru DigiNehru > /tmp/$file_name
