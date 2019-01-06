%1(start /min cmd.exe /c %0 :&exit)
set PROJECT_HOME=d:/TEST_CASE
cd /d %PROJECT_HOME%
java -jar selenium-server-standalone-3.8.1.jar -role node -port 5558 -hub http://172.16.3.220:4444/grid/register/