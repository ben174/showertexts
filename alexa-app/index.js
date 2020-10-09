var http       = require('http')
  , AlexaSkill = require('./AlexaSkill')
  , APP_ID     = 'amzn1.echo-sdk-ams.app.901a3f73-22df-4ad2-aa7c-ed49c3a07a6f'
  , MTA_KEY    = 'your-mta-key';

var url = 'http://www.showertexts.com/random';


var getThoughtText = function(callback){
  http.get(url, function(res){
    var body = '';

    res.on('data', function(data){
      body += data;
    });

    res.on('end', function(){
      var result = body;
      callback(result);
    });

  }).on('error', function(e){
    console.log('Error: ' + e);
  });
};

var handleNextRequest = function(intent, session, response){
  getThoughtText(function(data){
    var heading = 'Todays shower thought.';
    response.tellWithCard(data, heading, data);
  });
};


var ShowerText = function(){
  AlexaSkill.call(this, APP_ID);
};

ShowerText.prototype = Object.create(AlexaSkill.prototype);
ShowerText.prototype.constructor = ShowerText;

ShowerText.prototype.eventHandlers.onLaunch = function(launchRequest, session, response){
  getThoughtText(function(data){
    var heading = 'Todays shower thought.';
    response.tellWithCard(data, heading, data);
  });
};


ShowerText.prototype.intentHandlers = {
  GetThoughtIntent: function(intent, session, response){
    handleNextRequest(intent, session, response);
  },

  HelpIntent: function(intent, session, response){
    var speechOutput = 'To get todays shower thought, just say: Alexa, open Shower Thoughts.';
    response.tellWithCard(speechOutput, 'Help', speechOutput);
  }
};


exports.handler = function(event, context) {
    var skill = new ShowerText();
    skill.execute(event, context);
};
