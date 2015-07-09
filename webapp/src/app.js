import 'bootstrap';
import 'bootstrap/css/bootstrap.css!';

import 'materialize/dist/js/ripples'
import 'materialize'
import 'materialize/dist/css/roboto.css!'
import 'materialize/dist/css/material.css!'
import 'materialize/dist/css/ripples.css!'

export class App {
  configureRouter(config, router){
    config.title = 'Aurelia';
    config.map([
      { route: ['','welcome'], name: 'welcome',      moduleId: './welcome',      nav: true, title:'Welcome' },
      { route: 'flickr',       name: 'flickr',       moduleId: './flickr',       nav: true, title:'Flickr' },
      { route: 'child-router', name: 'child-router', moduleId: './child-router', nav: true, title:'Child Router' }
    ]);

    this.router = router;
  }
}
