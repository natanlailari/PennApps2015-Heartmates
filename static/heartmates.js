angular
    //div ngapp - HeartmatesApp
    .module('HeartmatesApp', [])

    //managae routes through the routeProvider
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            //when for specific cases  - use url and controller
            //loads in ngview
            .when('/', {
                templateUrl: '../static/index.html',
                controller: 'IndexController'
            })
            .when('/checkout', {
                templateUrl: '../static/checkout.html',
                controller: 'CheckoutController'
            })
            .when('/itemlist', {
                templateUrl: '../static/Whole_Foods.html',
                controller: 'ItemlistController'
            })
            .when('/cart', {
                templateUrl: '../static/cart.html',
                controller: 'CartController'
            })
            .otherwise({ redirectTo: '/' });
    }])
    .controller('IndexController', [
        '$scope', 
        '$http',
        'windowAlert',
        function($scope, $http, windowAlert) {
            $scope.RETRIEVE_DEFAULT_NR = 5;
            $scope.state = {};
            $scope.state.todoList = [];
            $scope.state.retrieveNr = $scope.RETRIEVE_DEFAULT_NR;

            $scope.addItem = function() {
                if (!$scope.state.newItem) {
                    windowAlert("text field must be non-empty");
                } else {
                    $http
                        .post('/todoAdd', {
                            item: $scope.state.newItem
                        })
                        .success(function(data, status, headers, config) {
                            if (data.success) {
                                $scope.retrieveLastNItems(
                                    $scope.state.retrieveNr
                                );
                            } else {
                                windowAlert('Adding of item failed');
                            }
                        })
                        .error(function(data, status, headers, config) {
                        });
                }
            };
        }
    ]);