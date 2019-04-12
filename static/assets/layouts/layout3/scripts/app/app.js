 function diffDate(date2, date1)
                 {

                      if (date1 == date2){
                          diffDays = 1
                          return diffDays
                      }else{
                      var date1 = new Date(date1);
                      var date2 = new Date(date2);
                      var timeDiff = Math.abs(date2.getTime() - date1.getTime());
                      var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                      return diffDays

                      }


                 }

var app = angular.module('roadapp', ['angularUtils.directives.dirPagination',])

app.config(function($httpProvider) {
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $httpProvider.defaults.headers.post['X-CSRFToken'] = token;
});

app.config(function ($locationProvider) {
    $locationProvider.html5Mode(true)
    $locationProvider.hashPrefix('!');
});

app.service('AccommodationService', function () {
           var service = {
                            accommodations: []
                          };
                          return service;
         });

 app.service('AdvanceService', function () {
           var service = {
                            advances: []
                          };
                          return service;
         });

 app.service('MultipleService', function () {
           var service = {
                            multiple: []
                          };
                          return service;
         });

  app.service('AdviceService', function () {
           var service = {
                            advices: []
                          };
                          return service;
         });


app.controller('AdController', function($scope, $http) {
            $http.get("/account/approval_api/")
                                            .success(function(response) {
                                            $scope.approvals = response;
                                            });
            $scope.sort= function(Keyname){
            $scope.sortKey = Keyname;
            $scope.reverse = !$scope.reverse;

            }
});

app.controller('MyApprovalController', function($scope, $http) {
            $http.get("/account/approval_api/my/")
                                            .success(function(response) {
                                            $scope.approvals = response;
                                            });
            $scope.sort= function(Keyname){
            $scope.sortKey = Keyname;
            $scope.reverse = !$scope.reverse;

            }
});


app.controller('AdviceController', function($scope, $http, $sce, $location, AdviceService) {
            $scope.ShowGif=false;
             //alert('testing');
            $scope.processForm = function() {
                  $scope.ShowGif=true;
                  $http({
                  method  : 'POST',
                  url     : '/travel/advice/',
                  data    : $.param({
                            travel_advice: JSON.stringify($scope.advices),
                            postdetails:$scope.postdetails
                  }),  // pass in data as strings
                  headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
                 })
                  .success(function(data) {
                    //console.log(data);
                      //$scope.showTheForm=false;
                      $scope.Message=$sce.trustAsHtml(data);
                      $scope.ShowGif=false

                      //$location.path('/travel/test/');
                  });
                };

            $scope.postdetails = postdetails;
            $scope.advices = AdviceService.advices;
            $scope.newAdvice = {};

             $scope.addAdvice = function() {
               if( $scope.location_name === '' || $scope.location_name == undefined){
                  swal("Please enter location" + location_name);
                  return;
                }else if($scope.hotel === '' || $scope.hotel == undefined){
                  swal('Please enter the hotel');
                  return;
                }
                else if($scope.address === '' || $scope.address == undefined){
                  swal('Please enter the address');
                  return;
                }
                else{
                    //alert($scope.location_name);
                    $scope.newAdvice.location = $scope.location_name;
                    $scope.newAdvice.hotel = $scope.hotel;
                    $scope.newAdvice.address = $scope.address;


                 AdviceService.advices.push($scope.newAdvice);
                 $scope.newAdvice = {};

                }
              }

             $scope.deleteAdvice = function(advice)
              {
                 AdviceService.advices.pop(advice);
                 console.log("Delete " + advice)
              }

         });

app.controller('RoadController', function($scope, $http, $sce, $location, AccommodationService, AdvanceService) {

            $scope.showTheForm=true;
            //$scope.ShowMessage=false;
            $scope.ShowGif = false;
            $scope.ShowMileage = true;
            $scope.showGroup=false;

            $http.get("/travel/list/")
                .success(function(response) {$scope.names = response;});

            $http.get("/travel/listadv/")
                .success(function(response) {$scope.adv = response;});

            $http.get("/travel/group/"+postdetails)
            .success(function(response) {$scope.groups = response;});

            if(check=="True"){ $scope.showGroup=true; }

            $scope.processForm = function() {
                  $scope.ShowGif=true;
                  $http({
                  method  : 'POST',
                  url     : '/travel/roadadd/',
                  data    : $.param({
                            departure_location: $scope.departure_location,
                            destination_location: $scope.destination_location,
                            mileage: $scope.mileage,
                            departure_date: $scope.departure_date,
                            accommodation: JSON.stringify($scope.accommodations),
                            advance:JSON.stringify($scope.advances),
                            mileage_cost:parseFloat($scope.MileageCost).toFixed(2),
                            postdetails:$scope.postdetails,
                            accomodation_rate: $scope.accomodation_cost,
                            flight_rate: $scope.mileage_allowed,
                            flight_units: $scope.mileage,
                            f_type : $scope.ShowMileage,
                            totalEstimated : parseFloat($scope.reduceTotal()).toFixed(2),
                            totalAdvance : parseFloat($scope.getAdvanceTotal()).toFixed(2)

                  }),  // pass in data as strings
                  headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
                 })
                  .success(function(data) {
                    //console.log(data);
                      $scope.showTheForm=false;
                      $scope.Message=$sce.trustAsHtml(data);
                      $scope.ShowGif=false

                      //$location.path('/travel/test/');
                  }).error(function(error) {
                        //$scope.showTheForm=false;
                        $scope.Message=$sce.trustAsHtml("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>");
                        $scope.ShowGif=false
                    });
                };

            $scope.postdetails = postdetails;
            $scope.mileage_allowed = 50
            $scope.accomodation_cost = accomodation_cost;
            $scope.parseInt = parseInt;
            $scope.MileageCost = function(){
             return (parseInt($scope.mileage) * 50)
            }

            $scope.Currency = function(amount)
            {
               return parseFloat(amount).toFixed(2)
            }
            //$scope.mileage_cost = $scope.mileage; //parseInt($scope.mileage * 50);
            $scope.accommodations = AccommodationService.accommodations;
            $scope.getTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                for(var i = 0; i < $scope.accommodations.length; i++){
                    console.log('ft' + $scope.accommodations[i].diff)
                    var diff = $scope.accommodations[i].diff;
                    total += (diff * $scope.accomodation_cost);
                }
                return parseInt(total);
            }

             $scope.addAccommodation = function() {
               if($scope.newAccommodation.name === '' || $scope.newAccommodation.name == undefined){
                  swal("Please enter accomodation location");
                  return;
                }else if($scope.newAccommodation.check_in_date === '' || $scope.newAccommodation.check_in_date == undefined){
                  swal('Please select check in date');
                  return;
                }
                else if($scope.newAccommodation.check_out_date === '' || $scope.newAccommodation.check_out_date == undefined){
                  swal('Please select check out date');
                  return;
                }
                else{

                $scope.newAccommodation.diff = diffDate($scope.newAccommodation.check_out_date, $scope.newAccommodation.check_in_date);
                AccommodationService.accommodations.push($scope.newAccommodation);
                $scope.newAccommodation = {};

                }
              }

             $scope.deleteAccommodation = function(accommodation)
              {
                 AccommodationService.accommodations.pop(accommodation);
                 console.log("Delete " + accommodation)
              }

            $scope.getAdvanceTotal = function(){
                var total = 0;
                console.log('check total' + $scope.advances.length)
                for(var i = 0; i < $scope.advances.length; i++){
                    console.log('ft' + $scope.advances[i].cost)
                    var cost = $scope.advances[i].cost;
                    total += cost;
                }
                return total;
            }
            $scope.advances = AdvanceService.advances;
            $scope.addAdvance = function() {
                if ($scope.newAdvance.units === '' || $scope.newAdvance.units == undefined) {
                    swal("Please enter advance units");
                    return;
                } else if ($scope.newAdvance.rate === '' || $scope.newAdvance.rate == undefined) {
                    swal('Please enter  advance rate');
                    return;
                }
                else {
                    // alert($scope.newAdvance.advance_description);
                    if ($scope.newAdvance.advance_description == 'Mileage'){

                        $scope.ShowMileage = false;
                    }
                    $scope.newAdvance.cost = $scope.newAdvance.units * $scope.newAdvance.rate;
                    console.log($scope.newAdvance)
                    AdvanceService.advances.push($scope.newAdvance);
                    $scope.newAdvance = {};

                }
            }

            $scope.deleteAdvance = function(advance){
                    AdvanceService.advances.pop(advance);
                    console.log("Delete Advance" + advance );
            }

            $scope.reduceTotal = function(){
            var subEstTotal = 0;
                if($scope.ShowMileage){
                    subEstTotal = $scope.getTotal() + $scope.MileageCost() +  $scope.getAdvanceTotal();
                }else{
                    subEstTotal = $scope.getTotal() +  $scope.getAdvanceTotal();
                }
                    return subEstTotal;

            }

         });


app.controller('OneWayController', function($scope, $http, $sce, $location, AccommodationService, AdvanceService) {

            $scope.showTheForm=true;
            $scope.ShowMessage=false;
            $scope.ShowGif =false;
            $scope.ShowFlght = true;
            $scope.showGroup=false;

            if (travel_type=="National"){
                $scope.ShowFlightCost=false;
                $scope.flight_cost=35000;
            }else
            {
                  $scope.ShowFlightCost=true;
            }
            $http.get("/travel/list/")
                .success(function(response) {$scope.names = response;});

            $http.get("/travel/listadv/")
                .success(function(response) {$scope.adv = response;});

            $http.get("/travel/group/"+postdetails)
                .success(function(response) {$scope.groups = response;});

            if(check=="True"){ $scope.showGroup=true; }

            $scope.processForm = function() {
            $scope.ShowGif =true;
                  $http({
                  method  : 'POST',
                  url     : '/travel/onewaytrip/',
                  data    : $.param({
                           departure_location: $scope.departure_airport,
                           destination_location: $scope.destination_airport,
                           flight_cost: $scope.flight_cost,
                           departure_date: $scope.departure_date,
                           accommodation: JSON.stringify($scope.accommodations),
                           advance:JSON.stringify($scope.advances),
                           postdetails: $scope.postdetails,
                           accomodation_rate: $scope.accomodation_cost,
                           flight_rate: $scope.flight_cost,
                           f_type : $scope.ShowFlght,
                           flight_units: 1,
                           totalEstimatedNaira : $scope.Currency($scope.reduceTotal()),
                           totalEstimatedDollar: $scope.Currency($scope.parseFloat($scope.getDollarTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Dollar)),
                           totalAdvanceDollar : $scope.Currency($scope.getAdvanceTotal().Dollar),
                           totalAdvanceNaira : $scope.Currency($scope.getAdvanceTotal().Naira)
                  }),  // pass in data as strings
                  headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
                 })
                  .success(function(data) {
                    //console.log(data);
                      $scope.showTheForm=false;
                      $scope.Message=$sce.trustAsHtml(data);
                      $scope.ShowGif=false

                      //$location.path('/travel/test/');
                  }).error(function(error) {
                        $scope.showTheForm=true;
                        $scope.Message=$sce.trustAsHtml("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>");
                        $scope.ShowGif=false
                    });
                };

            $scope.postdetails = postdetails;
            $scope.travel_type = travel_type;
            $scope.accomodation_cost = accomodation_cost;
            $scope.parseInt = parseInt;
            $scope.parseFloat = parseFloat;
            $scope.accommodations = AccommodationService.accommodations;

            $scope.Currency = function(amount)
            {
               return parseFloat(amount).toFixed(2)
            }

            $scope.getDollarTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                if (travel_type!="National"){

                for(var i = 0; i < $scope.accommodations.length; i++){
                    var diff = $scope.accommodations[i].diff;
                    console.log(diff)
                    total += (diff * $scope.accomodation_cost);
                    console.log(total)
                }
                }

                return total;

            }

            $scope.getNairaTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                if (travel_type=="National"){

                for(var i = 0; i < $scope.accommodations.length; i++){
                    var diff = $scope.accommodations[i].diff;
                    console.log(diff)
                    total += (diff * $scope.accomodation_cost);
                    console.log(total)
                }
                }
                console.log("Naira" + total);
                return total;

            }


           if(travel_type=="National")
            {
              $scope.ShowNaira="₦"
            }else{

              $scope.ShowDollar="$"

            }

            function getNum(val) {
               if (isNaN(val)) {
                 return 0;
               }
               return val;
              }

            $scope.addAccommodation = function() {
                if($scope.newAccommodation.name === '' || $scope.newAccommodation.name == undefined){
                  swal("Please enter accomodation location");
                  return;
                }else if($scope.newAccommodation.check_in_date === '' || $scope.newAccommodation.check_in_date == undefined){
                  swal('Please select check in date');
                  return;
                }
                else if($scope.newAccommodation.check_out_date === '' || $scope.newAccommodation.check_out_date == undefined){
                  swal('Please select check out date');
                  return;
                }
                else{
                $scope.newAccommodation.diff = diffDate($scope.newAccommodation.check_out_date, $scope.newAccommodation.check_in_date);
                AccommodationService.accommodations.push($scope.newAccommodation);
                $scope.newAccommodation = {};

                }
              }

             $scope.deleteAccommodation = function(accommodation)
              {
                 AccommodationService.accommodations.pop(accommodation);
                 console.log("Delete " + accommodation)
              }

            $scope.getAdvanceTotal = function(){
                var total = 0;
                var newTotal={"Dollar": 0, "Naira":0 };
                console.log('check total' + $scope.advances.length)
                for(var i = 0; i < $scope.advances.length; i++){
                    //console.log('ft' + $scope.advances[i].cost)
                    console.log($scope.advances[i].currency)
                    if ($scope.advances[i].currency=="USD"){
                    newTotal.Dollar+=$scope.advances[i].cost;

                    }
                    else{
                    newTotal["Naira"] +=$scope.advances[i].cost;
                    console.log(newTotal["Naira"])

                    }

                }
                return newTotal;
            }

            $scope.advances = AdvanceService.advances;
            $scope.addAdvance = function() {

                if ($scope.newAdvance.units === '' || $scope.newAdvance.units == undefined) {
                    swal("Please enter advance units");
                    return;
                } else if ($scope.newAdvance.rate === '' || $scope.newAdvance.rate == undefined) {
                    swal('Please enter  advance rate');
                    return;
                }
                else {
                    if ($scope.newAdvance.advance_description == 'Flight'){

                        $scope.ShowFlght = false;
                    }
                    $scope.newAdvance.cost = $scope.newAdvance.units * $scope.newAdvance.rate;
                    console.log($scope.newAdvance)
                    AdvanceService.advances.push($scope.newAdvance);
                    $scope.newAdvance = {};
                }
            }
                $scope.deleteAdvance = function(advance){
                     AdvanceService.advances.pop(advance)
                     console.log("Delete Advance" + advance )
                }

        //      $scope.people = [
        //     {firstName: "Daryl", surname: "Rowland", twitter: "@darylrowland", pic: "img/daryl.jpeg"},
        //     {firstName: "Alan", surname: "Partridge", twitter: "@alangpartridge", pic: "img/alanp.jpg"},
        //     {firstName: "Annie", surname: "Rowland", twitter: "@anklesannie", pic: "img/annie.jpg"}
        // ];

        // $scope.countries = [{"name": "Lagos", "id": 1}, {"name": "Lagos international airport", "id": 3}];

                 $scope.reduceTotal = function(){
                    var subEstTotal = 0;
                        if($scope.ShowMileage){
                            subEstTotal = $scope.parseFloat($scope.flight_cost) + $scope.parseFloat($scope.getNairaTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Naira);
                        }else{
                            subEstTotal =  $scope.parseFloat($scope.getNairaTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Naira);
                        }
                         return subEstTotal;

                  }


         });


app.controller('ReturnController', function($scope, $http, $sce, AccommodationService, AdvanceService) {

            $scope.showTheForm=true;
            $scope.ShowMessage=false;
            $scope.ShowGif =false;
            $scope.ShowFlght = true;
            $scope.showGroup =false;

            if (travel_type=="National"){
            $scope.ShowFlightCost=false;
            $scope.flight_cost=35000;
            }else
            {
            $scope.ShowFlightCost=true;
            }

            $http.get("/travel/list/")
                .success(function(response) {$scope.names = response;});

            $http.get("/travel/listadv/")
                .success(function(response) {$scope.adv = response;});


            $http.get("/travel/group/"+postdetails)
                .success(function(response) {$scope.groups = response;});
            
            if(check=="True"){ $scope.showGroup=true; }

            $scope.processForm = function() {
                 $scope.ShowGif =true;
                  $http({
                  method  : 'POST',
                  url     : '/travel/returntrip/',
                  data    : $.param({
                           departure_location: $scope.departure_airport,
                           destination_location: $scope.destination_airport,
                           flight_cost: $scope.flight_cost,
                           departure_date: $scope.departure_date,
                           return_departure_date: $scope.return_departure_date,
                           //return_arrival_date: $scope.return_departure_date,
                           accommodation: JSON.stringify($scope.accommodations),
                           advance:JSON.stringify($scope.advances),
                           postdetails:$scope.postdetails,
                           accomodation_rate: $scope.accomodation_cost,
                           flight_rate: $scope.flight_cost,
                           f_type : $scope.ShowFlght,
                           flight_units: 2,
                           totalEstimatedNaira : $scope.Currency($scope.reduceTotal()),
                           totalEstimatedDollar: $scope.Currency($scope.parseFloat($scope.getDollarTotal()) +  $scope.parseFloat($scope.getAdvanceTotal().Dollar)),
                           totalAdvanceDollar : $scope.Currency($scope.getAdvanceTotal().Dollar),
                           totalAdvanceNaira : $scope.Currency($scope.getAdvanceTotal().Naira)
                  }),  // pass in data as strings
                  headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
                 })
                  .success(function(data) {
                    //console.log(data);
                      $scope.showTheForm=false;
                      $scope.Message=$sce.trustAsHtml(data);
                      $scope.ShowGif=false

                      //$location.path('/travel/test/');
                  }).error(function(error) {
                        //$scope.showTheForm=false;
                        $scope.Message=$sce.trustAsHtml("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>");
                        $scope.ShowGif=false
                    });
                };

            $scope.postdetails = postdetails;
            $scope.travel_type = travel_type;
            $scope.accomodation_cost = accomodation_cost;
            $scope.parseInt = parseInt;
            $scope.parseFloat = parseFloat;
            $scope.accommodations = AccommodationService.accommodations;

           $scope.Currency = function(amount)
            {
               return parseFloat(amount).toFixed(2)
            }

           $scope.FlightCost= function()
           {
              return parseInt($scope.flight_cost) * 2
           }

            $scope.getDollarTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                if (travel_type!="National"){

                for(var i = 0; i < $scope.accommodations.length; i++){
                    var diff = $scope.accommodations[i].diff;
                    console.log(diff)
                    total += (diff * $scope.accomodation_cost);
                    console.log(total)
                }
                }

                return total;

            }

            $scope.getNairaTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                if (travel_type=="National"){

                for(var i = 0; i < $scope.accommodations.length; i++){
                    var diff = $scope.accommodations[i].diff;
                    console.log(diff)
                    total += (diff * $scope.accomodation_cost);
                    console.log(total)
                }
                }
                console.log("Naira" + total);
                return total;

            }


           if(travel_type=="National")
            {
              $scope.ShowNaira="₦"
            }else{

              $scope.ShowDollar="$"

            }

            function getNum(val) {
               if (isNaN(val)) {
                 return 0;
               }
               return val;
              }

           $scope.addAccommodation = function() {
                if($scope.newAccommodation.name === '' || $scope.newAccommodation.name == undefined){
                  swal("Please enter accomodation location");
                  return;
                }else if($scope.newAccommodation.check_in_date === '' || $scope.newAccommodation.check_in_date == undefined){
                  swal('Please select check in date');
                  return;
                }
                else if($scope.newAccommodation.check_out_date === '' || $scope.newAccommodation.check_out_date == undefined){
                  swal('Please select check out date');
                  return;
                }
                else{
                $scope.newAccommodation.diff = diffDate($scope.newAccommodation.check_out_date, $scope.newAccommodation.check_in_date);
                AccommodationService.accommodations.push($scope.newAccommodation);
                $scope.newAccommodation = {};

                }
              }

             $scope.deleteAccommodation = function(accommodation)
              {
                 AccommodationService.accommodations.pop(accommodation);
                 console.log("Delete " + accommodation)
              }

            $scope.getAdvanceTotal = function(){
                var total = 0;
                var newTotal={"Dollar": 0, "Naira":0 };
                console.log('check total' + $scope.advances.length)
                for(var i = 0; i < $scope.advances.length; i++){
                    //console.log('ft' + $scope.advances[i].cost)
                    console.log($scope.advances[i].currency)
                    if ($scope.advances[i].currency=="USD"){
                    newTotal.Dollar+=$scope.advances[i].cost;

                    }
                    else{
                    newTotal["Naira"] +=$scope.advances[i].cost;
                    console.log(newTotal["Naira"])

                    }

                }
                return newTotal;
            }
            $scope.advances = AdvanceService.advances;

            $scope.addAdvance = function() {
                if ($scope.newAdvance.units === '' || $scope.newAdvance.units == undefined) {
                    swal("Please enter advance units");
                    return;
                } else if ($scope.newAdvance.rate === '' || $scope.newAdvance.rate == undefined) {
                    swal('Please enter  advance rate');
                    return;
                }
                else {
                     if ($scope.newAdvance.advance_description == 'Flight'){

                        $scope.ShowFlght = false;
                    }
                    $scope.newAdvance.cost = $scope.newAdvance.units * $scope.newAdvance.rate;
                    console.log($scope.newAdvance)
                    AdvanceService.advances.push($scope.newAdvance);
                    $scope.newAdvance = {};
                }
            }

                $scope.deleteAdvance = function(advance){
                     AdvanceService.advances.pop(advance)
                     console.log("Delete Advance" + advance )
                }

          $scope.reduceTotal = function(){
                    var subEstTotal = 0;
                        if($scope.ShowMileage){
                            subEstTotal = $scope.parseFloat($scope.FlightCost()) + $scope.parseFloat($scope.getNairaTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Naira);
                        }else{
                            subEstTotal = $scope.parseFloat($scope.getNairaTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Naira);
                        }
                         return subEstTotal;

                  }

         });


app.controller('MultipleController', function($scope, $http, $sce ,AccommodationService, AdvanceService, MultipleService) {

            $scope.showTheForm=true;
            $scope.ShowMessage=false;
            $scope.ShowGif =false;
            $scope.ShowFlght = true;
            $scope.showGroup = false;

            if (travel_type=="National"){
            $scope.ShowFlightCost=false;
            $scope.flight_cost=35000;
            }else
            {
            $scope.ShowFlightCost=true;
        }

            $http.get("/travel/list/")
                .success(function(response) {$scope.names = response;});

            $http.get("/travel/listadv/")
                .success(function(response) {$scope.adv = response;});

            $http.get("/travel/group/"+postdetails)
                .success(function(response) {$scope.groups = response;});
            
            if(check=="True"){ $scope.showGroup=true; }

            $scope.processForm = function() {
                $scope.ShowGif =true;
                  $http({
                  method  : 'POST',
                  url     : '/travel/multipletrip/',
                  data    : $.param({
                           flight : JSON.stringify($scope.multiple),
                           accommodation: JSON.stringify($scope.accommodations),
                           advance:JSON.stringify($scope.advances),
                           postdetails:$scope.postdetails,
                           accomodation_rate: $scope.accomodation_cost,
                           flight_rate: $scope.flight_cost,
                           f_type : $scope.ShowFlght,
                           flight_units: $scope.multiple.length,
                           totalEstimatedNaira : $scope.Currency($scope.reduceTotal()),
                           totalEstimatedDollar: $scope.Currency($scope.parseFloat($scope.getDollarTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Dollar)),
                           totalAdvanceDollar : $scope.Currency($scope.getAdvanceTotal().Dollar),
                           totalAdvanceNaira : $scope.Currency($scope.getAdvanceTotal().Naira)

                  }),  // pass in data as strings
                  headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
                 })
                  .success(function(data) {
                    //console.log(data);
                      $scope.showTheForm=false;
                      $scope.Message=$sce.trustAsHtml(data);
                      $scope.ShowGif=false

                      //$location.path('/travel/test/');
                  }).error(function(error) {
                        //$scope.showTheForm=false;
                        $scope.Message=$sce.trustAsHtml("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>");
                        $scope.ShowGif=false
                    });
                };

            $scope.postdetails = postdetails;
            $scope.accomodation_cost = accomodation_cost;
            $scope.parseInt = parseInt;
            $scope.parseFloat = parseFloat;
            $scope.accommodations = AccommodationService.accommodations;

           $scope.Currency = function(amount)
            {
               return parseFloat(amount).toFixed(2)
            }

            $scope.multiple = MultipleService.multiple;

            $scope.addMultiple = function(){
             //accommodationService.accommodations.push($scope.newAccommodation);
                 $scope.newMultiple.flight_cost = $scope.flight_cost;
                 MultipleService.multiple.push($scope.newMultiple);
                 $scope.newMultiple = {};
            }

            $scope.getFlightTotal = function(){
                var total = 0;
                console.log('check total flight' + $scope.multiple.length)
                if (travel_type="National"){
                for(var i = 0; i < $scope.multiple.length; i++){
                    total += ($scope.multiple[i].flight_cost);
                    console.log(total)
                }
                }else
                {
                 for(var i = 0; i < $scope.multiple.length; i++){
                    total += ($scope.multiple[i].flight_cost);
                    console.log(total)
                }
                }
                return total;
            }

            $scope.getDollarTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                if (travel_type!="National"){

                for(var i = 0; i < $scope.accommodations.length; i++){
                    var diff = $scope.accommodations[i].diff;
                    console.log(diff)
                    total += (diff * $scope.accomodation_cost);
                    console.log(total)
                }
                }
                return total;
            }

            $scope.getNairaTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                if (travel_type=="National"){

                for(var i = 0; i < $scope.accommodations.length; i++){
                    var diff = $scope.accommodations[i].diff;
                    console.log(diff)
                    total += (diff * $scope.accomodation_cost);
                    console.log(total)
                }
                }
                console.log("Naira" + total);
                return total;

            }


           if(travel_type=="National")
            {
              $scope.ShowNaira="₦"
            }else{

              $scope.ShowDollar="$"

            }

            function getNum(val) {
               if (isNaN(val)) {
                 return 0;
               }
               return val;
              }

            $scope.addAccommodation = function() {
                if($scope.newAccommodation.name === '' || $scope.newAccommodation.name == undefined){
                  swal("Please enter accomodation location");
                  return;
                }else if($scope.newAccommodation.check_in_date === '' || $scope.newAccommodation.check_in_date == undefined){
                  swal('Please select check in date');
                  return;
                }
                else if($scope.newAccommodation.check_out_date === '' || $scope.newAccommodation.check_out_date == undefined){
                  swal('Please select check out date');
                  return;
                }
                else{
                $scope.newAccommodation.diff = diffDate($scope.newAccommodation.check_out_date, $scope.newAccommodation.check_in_date);
                AccommodationService.accommodations.push($scope.newAccommodation);
                $scope.newAccommodation = {};

                }
              }

             $scope.deleteAccommodation = function(accommodation)
              {
                 AccommodationService.accommodations.pop(accommodation);
                 console.log("Delete " + accommodation)
              }

            $scope.getAdvanceTotal = function(){
                var total = 0;
                var newTotal={"Dollar": 0, "Naira":0 };
                console.log('check total' + $scope.advances.length)
                for(var i = 0; i < $scope.advances.length; i++){
                    //console.log('ft' + $scope.advances[i].cost)
                    console.log($scope.advances[i].currency)
                    if ($scope.advances[i].currency=="USD"){
                    newTotal.Dollar+=$scope.advances[i].cost;

                    }
                    else{
                    newTotal["Naira"] +=$scope.advances[i].cost;
                    console.log(newTotal["Naira"])

                    }

                }
                return newTotal;
            }

            $scope.advances = AdvanceService.advances;
            $scope.addAdvance = function() {
                if ($scope.newAdvance.units === '' || $scope.newAdvance.units == undefined) {
                    swal("Please enter advance units");
                    return;
                } else if ($scope.newAdvance.rate === '' || $scope.newAdvance.rate == undefined) {
                    swal('Please enter  advance rate');
                    return;
                }
                else {
                     if ($scope.newAdvance.advance_description == 'Flight'){

                        $scope.ShowFlght = false;
                    }
                    $scope.newAdvance.cost = $scope.newAdvance.units * $scope.newAdvance.rate;
                    console.log($scope.newAdvance)
                    AdvanceService.advances.push($scope.newAdvance);
                    $scope.newAdvance = {};
                }
            }
                $scope.deleteAdvance = function(advance){
                     AdvanceService.advances.pop(advance);
                     console.log("Delete Advance" + advance);
                }

                 $scope.reduceTotal = function(){
                    var subEstTotal = 0;
                        if($scope.ShowMileage){
                            subEstTotal = $scope.parseFloat($scope.getFlightTotal()) + $scope.parseFloat($scope.getNairaTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Naira);
                        }else{
                            subEstTotal =  $scope.parseFloat($scope.getNairaTotal()) + $scope.parseFloat($scope.getAdvanceTotal().Naira);
                        }
                         return subEstTotal;

                  }

         });

