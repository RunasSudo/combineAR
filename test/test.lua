-- For the OpenDKIM miltertest tool
-- ./miltertest -v -s test.lua

--mt.startfilter("/usr/bin/python2", "../main.py")
--mt.sleep(1)

local conn = mt.connect('unix:/tmp/combinear.sock')
mt.header(conn, 'Subject', 'Hello World')
mt.header(conn, 'Authentication-Results', 'example.com;\r\n\tdkim=pass (2048-bit key) header.d=twitter.com header.i=@twitter.com header.b=aY/jKOIb')
mt.header(conn, 'Authentication-Results', 'example.com; dmarc=pass header.from=twitter.com')
mt.header(conn, 'Authentication-Results', 'example.com; spf=pass (sender SPF authorized) smtp.mailfrom=bounce.twitter.com (client-ip=199.59.150.95; helo=spruce-goose-az.twitter.com; envelope-from=b013614b853twitter=yingtongli.me@bounce.twitter.com; receiver=jsmith@example.com)')
mt.bodystring(conn, 'Hello World! This is a test email!')
mt.eom(conn)

if not mt.eom_check(conn, MT_HDRADD, "Authentication-Results") then
	error "No header added."
end

print(mt.getheader(conn, "Authentication-Results", 0))
