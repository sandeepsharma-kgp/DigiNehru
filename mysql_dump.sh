now=$(date +'%Y-%m-%d')
yesterday=$(date  -d "1 day ago" +'%Y-%m-%d')
file_name="$now.sql"
delete_file="$yesterday.sql"
rm -rf ~/Dump/$delete_file
mysqldump -u root -pdigitalnehru DigiNehru > ~/Dump/$file_name
