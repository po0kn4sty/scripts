require 'etsy'

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

