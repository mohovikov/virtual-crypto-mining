function parseBBCode(input) {
  let text = input;

  // Escape HTML
  text = text.replace(/&/g, "&amp;")
              .replace(/</g, "&lt;")
              .replace(/>/g, "&gt;");

  const rules = [
      [/\[b\](.*?)\[\/b\]/gi, '<b>$1</b>'],
      [/\[i\](.*?)\[\/i\]/gi, '<i>$1</i>'],
      [/\[u\](.*?)\[\/u\]/gi, '<u>$1</u>'],
      [/\[s\](.*?)\[\/s\]/gi, '<s>$1</s>'],
      [/\[url\](.*?)\[\/url\]/gi, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'],
      [/\[url=(.*?)\](.*?)\[\/url\]/gi, '<a href="$1" target="_blank" rel="noopener noreferrer">$2</a>'],
      [/\[img\](.*?)\[\/img\]/gi, '<img src="$1" class="img-fluid">'],
      [/\[img=(.*?)\](.*?)\[\/img\]/gi, '<img src="$1" alt="$2" title="$2" class="img-fluid">'],
      [/\[center\](.*?)\[\/center\]/gi, '<div class="text-center">$1</div>'],
      [/\[color=(.*?)\](.*?)\[\/color\]/gi, '<span style="color: $1;">$2</span>'],
      [/\[size=(\d+)\](.*?)\[\/size\]/gi, '<span style="font-size: calc(0.5rem + $1 * 2px);">$2</span>'],
      [/\[quote\](.*?)\[\/quote\]/gis, '<blockquote class="blockquote"><p>$1</p></blockquote>'],
      [/\[quote=(.*?)\](.*?)\[\/quote\]/gis, '<figure><blockquote class="blockquote">$2</blockquote><figcaption class="blockquote-footer">сказал $1</figcaption></figure>'],
      [/\[quote name=(.*?)\](.*?)\[\/quote\]/gis, '<figure><blockquote class="blockquote">$2</blockquote><figcaption class="blockquote-footer">сказал $1</figcaption></figure>'],
      [/\[code\](.*?)\[\/code\]/gis, '<pre><code>$1</code></pre>'],
  ];

  for (let [pattern, replacement] of rules) {
      text = text.replace(pattern, replacement);
  }

  return text;
}