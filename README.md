# TOAS_room_notifier
check TOAS Quickly available apartments webpage and send a notification email if the information updated

The requirements are simple: I am currently looking for a new apartment. At first, you need to send TOAS an application and you will be in a queue. But there are sometimes also randomly available apartments due to someone didn't extend their contracts. So it is possible to get a suitable apartment in the 'Quickly available apartments' page. In order to keep the eyes on that page, here comes this script. 

The idea is very straightforward: Check the webpage once an hour (or any other time) and if there is information updated, then send an notification email 

How to do it?

1. Get the web page content - urllib2
2. Parse the content - HTMLParser
3. Send email - smtplib (gmail)
4. Check information update - hashlib
5. Periodically check the web page - crontab

Tips:

1. To use Gmail, you need to turn on 'Allow less secure apps' in 'Sign-in & security -> Connected apps & sites' in your google account
2. Set up you own crontab: 'crontab -e' and put '0 * * * *  /path/to/executable' there
