require 'etsy'
require 'mechanize'
require 'json'
=begin
Etsy.api_key = 'key'
Etsy.api_secret = 'secret'
request = Etsy.request_token
 - Paste in Browser - 
Etsy.verification_url
access = Etsy.access_token(request.token, request.secret, 'CODE')
Etsy.myself(access.token, access.secret)
auth = {:access_token => access.token, :access_secret => access.secret}
Etsy::Receipt.find_all_by_shop_id(shop_id, auth) -- returns json response
*
{:access_token=>"07dafdd84601fb52790285524515cc", :access_secret=>"d96256e7f3"}
=end

Etsy.api_key = 'rp3gukrevdtgq1aonmf3nrbq'
Etsy.api_secret = '1nq73iuy6o'

request = Etsy.request_token
puts Etsy.verification_url
my_code = gets.chomp

access = Etsy.access_token(request.token, request.secret, my_code) 
Etsy.myself(access.token, access_secret)
auth = {:access_token => access.token , :access_secret => access.secret}
#auth = {:access_token=>"07dafdd84601fb52790285524515cc", :access_secret=>"d96256e7f3"}

puts "so far so good"

myjson = Etsy::Receipt.find_all_by_shop_id('caresspress', auth)
parsed = JSON.parse(myjson[0])


puts "last chance to fail"
File.open('EtsyReceipts.json', 'w') { |f| JSON.dump(parsed, f) }
