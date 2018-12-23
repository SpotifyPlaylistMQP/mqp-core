var http = require('http')
    , fs = require('fs')
    , url = require('url')
    , port = 8080;

var server = http.createServer(function (req, res) {
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
        case '/run.html':
            sendFile(res, 'public/run.html')
            break
        case '/css/bootstrap.css':
            sendFile(res, 'public/css/bootstrap.css', 'text/css')
            break
        case '/css/style.css':
            sendFile(res, 'public/css/style.css', 'text/css')
            break
        case '/js/bootstrap.js':
            sendFile(res, 'public/js/bootstrap.js', 'text/javascript')
            break
        case '/js/popper.js':
            sendFile(res, 'public/js/popper.js', 'text/javascript')
            break
        case '/js/popper.min.js.map':
            sendFile(res, 'public/js/popper.min.js.map', 'text/javascript')
            break
        case '/js/bootstrap.min.js.map':
            sendFile(res, 'public/js/bootstrap.min.js.map', 'text/javascript')
            break
        case '/js/d3scripts.js':
            sendFile(res, 'public/js/d3scripts.js', 'text/javascript')
            break
        case '/css/bootstrap.min.css.map':
            sendFile(res, 'public/css/bootstrap.min.css.map', 'text/javascript')
            break
        case '/data/mf_mpd_square_100':
            sendFile(res, 'public/data/mf_mpd_square_100', 'text')
            break
        case '/data/feature_mf_mpd_square_100':
            sendFile(res, 'public/data/feature_mf_mpd_square_100', 'text')
            break
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
