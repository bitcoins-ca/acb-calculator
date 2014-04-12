
<!doctype html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Adjusted Cost Base Calculator</title>
        <link rel="stylesheet" type="text/css" media="screen" href="/static/landing-page/css/bootstrap.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="/static/landing-page/css/landing-page.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="/static/landing-page/font-awesome/css/font-awesome.css" />
        
        <script type="text/javascript" src="/static/js/jquery-1.10.2.min.js"></script>
        <script type="text/javascript" src="/static/landing-page/js/bootstrap.js"></script>
    </head>
    <body>
        
        <div class="intro-header">
    
            <div class="container">
                
                <div class="row">
                    <div class="col-md-8 col-md-offset-2">
                        <div class="intro-message">
                                        
                       
                            <h1>Adjusted Cost Base Calculator</h1>
                            <h3>A Bitcoin Hackathon Project</h3>
                            <hr class="intro-divider">
                            <ul class="list-inline intro-social-buttons">
                                <li><a href="https://twitter.com/trvrm" class="btn btn-default btn-lg"><i class="fa fa-twitter fa-fw"></i> <span class="network-name">Twitter</span></a>
                                </li>
                                
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-2 visible-md visible-lg">
                        <div class="intro-message">
                            <img  class="img-responsive" src="/static/img/Bitcoin.png" alt="">
                        </div>
                    </div>
                </div>
    
            </div>
            <!-- /.container -->
        </div>

        <div class="container">
        %if Helpers.error():
            <br>
            <div class="alert alert-danger">{{!Helpers.errormessage()}}</div>
        %end
        %if Helpers.info():
            <br>
            <div class="alert alert-info">{{!Helpers.infomessage()}}</div>
        %end
        </div>

    
        {{!base}}

        
        <footer>
            <div class="container">
                <div class="row">
                    <div class="col-lg-12">
                        <ul class="list-inline">
                            <li>
                                <a href="/">Home</a>
                            </li>
                            <li class="footer-menu-divider">⋅</li>
                            <li>
                                <a href="http://bitcoinexpo.ca/hackathon/">Bitcoin Expo Hackathon</a>
                            </li>
                            <li class="footer-menu-divider">⋅</li>
                            <li>
                                <a href="http://svy.ca/">Surveymedia</a>
                            </li>
                        </ul>
                        
                    </div>
                </div>
            </div>
        </footer>
    
    </body>
</html>
