%w(rubygems wordnik).each {|lib| require lib}
Wordnik.configure do |c|
  # c.api_key = '1d3baf57f57254b5c430200e729037e9dea9d87493f3a16b4'
  c.api_key = 'd92d8109432f0ead8000707303d0c6849e23be119a18df853'
  c.username = 'wordrainbow'
  c.password = 'gomer'
end
Wordnik.authenticate

list_permalink = "wordrainbow"
filename = 'colors.txt'

frequencies = File.readlines(filename).map do |color|
  body = Wordnik.word.get_frequency(:word => color.chomp)
  puts "#{color.chomp}: #{body['totalCount'].to_i}"
  {
    :word => color.chomp,
    :total => body['totalCount'].to_i
  }
end

# Sort the hashes, drop the counts, grab the words
words_by_frequency = frequencies.sort{ |x,y| x[:total] <=> y[:total] }.reverse.map {|w| w[:word]}

File.open("colors_by_frequency.txt", 'w') do |f|
  f.write(words_by_frequency.join("\n"))
end