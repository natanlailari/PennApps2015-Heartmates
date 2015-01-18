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
            })
            .when('/checkout', {
                templateUrl: '../static/checkout.html',
//                controller: 'ItemlistController'
            })
            .when('/itemlist', {
                templateUrl: '../static/Whole_Foods.html',
  //              controller: 'ItemlistController'
            })
            .when('/cart', {
                templateUrl: '../static/cart.html',
    //            controller: 'ItemlistController'
            })
            .otherwise({ redirectTo: '/' });
    }])
    .factory('windowAlert', [
        '$window',
        function($window) {
            return $window.alert;
        }
    ])

    .controller('ItemlistController', [
        '$scope', 
        '$http',
        'windowAlert',
        function($scope, $http, windowAlert) {
            $scope.state = {};
            $scope.state.itemsArray = [];
            $scope.state.address = "";
            $scope.state.fee = "";
            $scope.state.created = "";
            $scope.state.eta = "";
            $scope.state.finalList = [
            ];

            $scope.state.itemList = [
            {   name: "Bacon",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Broccoli",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Sliced Peaches",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "King Arthur Flour",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Quaker Steel Cut Oats",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Extra Virgin Oil",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Kendall Brooke Salmon",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Extra Firm Tofu",
                count: 0,
                tempCount: 0,
                score: 0
            },
            {   name: "Prairie Farms Milk",
                count: 0,
                tempCount: 0,
                score: 0
            }];

            console.log("called");

            $scope.increment = function(fooditem) {
                fooditem.tempCount++;
                return;
            };

            $scope.decrement = function(fooditem) {
                fooditem.tempCount--;
                if (fooditem.tempCount < 0) {
                    fooditem.tempCount = 0;
                }
                return;
            };

            $scope.addToCart = function(fooditem) {
                if (fooditem.tempCount != 0) {
                    fooditem.count = fooditem.tempCount;
                    console.log("added " + fooditem.tempCount + " to " + fooditem.name);
                    fooditem.tempCount = 0;
                }

            }

            $scope.firstCheckOut = function() {
                console.log("test");
                for (i = 0; i < $scope.state.itemList.length; i++) {
                    if ($scope.state.itemList[i].count != 0) {
                        $scope.state.itemsArray.push($scope.state.itemList[i].name);
                        console.log('test');
                    }
                }
                console.log($scope.state.itemsArray);

                $http
                    .post('/nutrition_facts/', {
                        items: $scope.state.itemsArray
                    })
                    .success(function(data, status, headers, config) {
                        console.log(data);
                        for (i = 0; i < data.scoreList; i++) {
                             $scope.state.itemList[data.scoreList[i].name] = data.scoreList[i].score;
                             item = {
                                name: data.scoreList[i].name,
                                score: data.scoreList[i].score
                             };
                             $scope.state.finalList.push(score);
                        }
                    })
                    .error(function(data, status, headers, config) {
                });
            };

            $scope.finalCheckOut = function() {
                $http
                    .get('/postmates_delivery/' + $scope.state.address)
                    .success(function(data, status, headers, config) {
                        $scope.state.fee = data.fee;
                        $scope.state.created = data.created;
                        $scope.state.eta = data.eta;
                    })
                    .error(function(data, status, headers, config) {
                    });
            };
        }
    ]);
