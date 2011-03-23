# Note: This script only works from a whitelisted IP (e.g. web1.wordnik.com)

%w(rubygems wordnik).each {|lib| require lib}
Wordnik.configure {|c| c.api_key = 'd92d8109432f0ead8000707303d0c6849e23be119a18df853'}

colors = []
lists = %w(
  chromatica
  color
  color-me-mauve
  color-my-words
  color-words-for-shoes 
  colorful-colors  
  colors--2
  colors--5
  colors--7
  colors--9
  colors-fantastic
  colour-me-happy
  crayola-old-style
  names-of-colours
  not-your-normal-colors
)

# Fetch blacklist array
blacklist = Wordnik::Request.new(:get, "wordList.json/blacklist/words").response.body.map{ |w| w['word'].downcase }

# Fetch each list and add its words to the colors array
lists.each do |list|
  request = Wordnik::Request.new(:get, "wordList.json/#{list}/words")
  request.response.body.each do |listed_word|
    word = listed_word['word'].downcase
    colors << word unless blacklist.include?(word)
  end
end

# Create an empty file for writing. If a file with the same name already exists its 
# content is erased and the file is treated as a new empty file.
File.open("colors.txt", 'w') {|f| f.write(colors.uniq.sort.join("\n")) }