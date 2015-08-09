$(function() {
  $("#subscribe").click(subscribe);
  setInterval(rotateThought, 6000);
});
thoughts = [
  'Waterboarding at Guantanamo Bay sounds super rad if you don\'t know what either of those things are.',
  'When Sweden is playing Denmark, it is SWE-DEN. The remaining letters, not used, is DEN-MARK.',
  'April Fool\'s Day is the one day of the year when people critically evaluate news articles before accepting them as true.',
  'I have never once hit the space bar while watching a YouTube video with the intention of scrolling halfway down the page',
  'Maybe "Are You Smarter Than a 5th Grader?" isn\'t a show that displays how stupid grown adults can be, but rather, a show that depicts how much useless information we teach grade schoolers that won\'t be retained or applicable later in life.',
  'The object of golf is to play the least amout of golf.',
  'Every time you upvote someone, you are making their day better, at the cost of nothing.',
  'I used hola unblocker to watch Argo on the Canadian Netflix. I was an American who had to pretend to be Canadian to watch a movie about Americans who have to pretend to be Canadians making a movie.',
  'instead of all the prequel and sequel movies coming out, they should start making equels - films shot in the same time period as the original film, but from an entirely different perspective',
  'Apple has "air." Amazon has "fire." Google has "earth." I think Microsoft should create something called "water."',
  'Now that cellphones are becoming more and more waterproof, pretty soon it will be okay to push people into pools again.',
  'X88B88 looks like the word voodoo reflecting off of itself.',
  '"Go to bed, you\'ll feel better in the morning" is the human version of "Did you turn it off and turn it back on again?"',
  'We should have a holiday called Space Day, where lights are to be shut off for at least an hour at night to reduce light pollution, so we can see the galaxy.',
  'Your shadow is a confirmation that light has traveled nearly 93 million miles unobstructed, only to be deprived of reaching the ground in the final few feet thanks to you.',
  'The sinking of the Titanic must have been a miracle to the lobsters in the kitchen.',
  'The person who would proof read Hitler\'s speeches was a grammar Nazi.',
]
var thoughtIndex = 0;
function rotateThought() {
  $("#thought").removeClass('bounceInRight').addClass('bounceOutLeft');
  setTimeout(moveInThought, 1000);
}
function moveInThought(){
  $("#thought").text(thoughts[thoughtIndex]).removeClass('bounceOutLeft').addClass('bounceInRight');
  thoughtIndex++;
  if(thoughtIndex > thoughts.length) {
    thoughtIndex = 0;
  }
}
function subscribe() {
  $("#heading").removeClass('rubberBand').addClass('bounceOutLeft');
  $.post("/subscribe", {'sms_number': $('#sms_number').val()}, function(data) {
    $("#heading").removeClass('bounceOutLeft').html("<a href='#'>" + data + "</a>").addClass('bounceInLeft');
  });
}