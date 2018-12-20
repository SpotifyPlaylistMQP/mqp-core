var http = require('http')
    , fs = require('fs')
    , url = require('url')
    , port = 8080;

var server = http.createServer(function (req, res) {
/*
    if(req.method == "POST"){
            res.writeHead(200, {"Content-Type":"application/javascript"});
            res.write('<h1> Example </h1>');
            res.end();
    }
*/
        /**
         If we have a post request.
         If we want to make multiple we need to specify the url ending ie
          if(req.url === '/getmydata'){
                handle a /getmydata request
          }
          if(req.url ==='/dootherthing'){

                handle a /dootherthing request
          }
         **/


        //add code to call function on req

    var uri = url.parse(req.url)
    //console.log('Fetching ' + uri.pathname + "!")
    switch (uri.pathname) {
        case '/':
            sendFile(res, 'public/index.html')
            break
        case '/index.html':
            sendFile(res, 'public/index.html')
            break
        case '/about.html':
            sendFile(res, 'public/about.html')
            break
        case '/matrixfactorization.html':
            sendFile(res, 'public/matrixfactorization.html')
            break
        // //fetches for CSS
        case '/css/bootstrap.css':
            sendFile(res, 'public/css/bootstrap.css', 'text/css')
            break
        case '/css/starter-template.css':
            sendFile(res, 'public/css/starter-template.css', 'text/css')
            break
        case '/data/mf_mpd_square_100.csv':
            sendFile(res, 'public/data/mf_mpd_square_100.csv', 'text/css')
            break
        // case '/vendor/bootstrap/css/bootstrap.min.css.map':
        //     sendFile(res, 'public/vendor/bootstrap/css/bootstrap.min.css.map', 'text/css')
        //     break
        // //fetches for img
        // case '/img/profile.jpg':
        //     sendFile(res, 'public/img/profile.jpg', 'img/jpg')
        //     break
        //fetches for JS
        case '/js/bootstrap.js':
            sendFile(res, 'public/js/bootstrap.js', 'text/javascript')
            break
        case '/js/popper.js':
            sendFile(res, 'public/js/popper.js', 'text/javascript')
            break
        // case '/vendor/bootstrap/js/bootstrap.bundle.min.js':
        //     sendFile(res, 'public/vendor/bootstrap/js/bootstrap.bundle.min.js', 'text/javascript')
        //     break
        // case '/vendor/bootstrap/js/bootstrap.bundle.min.js.map':
        //     sendFile(res, 'public/vendor/bootstrap/js/bootstrap.bundle.min.js.map', 'text/javascript')
        //     break
        // //fontawesome-free
        // case '/vendor/fontawesome-free/css/all.min.css':
        //     sendFile(res, 'public/vendor/fontawesome-free/css/all.min.css', 'text/css')
        //     break
        // case '/vendor/fontawesome-free/webfonts/fa-brands-400.woff2':
        //     sendFile(res, 'public/vendor/fontawesome-free/webfonts/fa-brands-400.woff2', 'font/woff2')
        //     break
        // case '/vendor/fontawesome-free/webfonts/fa-solid-900.woff2':
        //     sendFile(res, 'public/vendor/fontawesome-free/webfonts/fa-solid-900.woff2', 'font/woff2')
        //     break
        // case '/vendor/fontawesome-free/webfonts/fa-regular-400.woff2':
        //     sendFile(res, 'public/vendor/fontawesome-free/webfonts/fa-regular-400.woff2', 'font/woff2')
        //     break
        // case '/vendor/fontawesome-free/webfonts/fa-regular-400.woff':
        //     sendFile(res, 'public/vendor/fontawesome-free/webfonts/fa-regular-400.woff', 'font/woff')
        //     break
        // case '/vendor/fontawesome-free/webfonts/fa-regular-400.ttf':
        //     sendFile(res, '/vendor/fontawesome-free/webfonts/fa-regular-400.ttf', 'font/tff')
        //     break
        // //Vendor/jquery
        // case '/vendor/jquery/jquery.min.js':
        //     sendFile(res, 'public/vendor/jquery/jquery.min.js', 'text/javascript')
        //     break
        // //Vendor/jquery-easing
        // case '/vendor/jquery-easing/jquery.easing.min.js':
        //     sendFile(res, 'public/vendor/jquery-easing/jquery.easing.min.js', 'text/javascript')
        //     break
        default:
            console.log('Error 404 ' + uri.pathname + " not found!")
            res.end('404 not found')
    }
})

server.listen(process.env.PORT || port);
console.log('listening on 8080')

// subroutines
// NOTE: this is an ideal place to add your data functionality

function sendFile(res, filename, contentType) {
    contentType = contentType || 'text/html';

    fs.readFile(filename, function (error, content) {
        res.writeHead(200, {'Content-type': contentType})
        res.end(content, 'utf-8')
    })

}
