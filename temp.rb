File.open('EtsyAPI.ks', 'r') do |f|
  f.each do |line|
    puts line
  end
end 
File.open('asdf', 'w') do |f|
  f.write('testtest') 
end
