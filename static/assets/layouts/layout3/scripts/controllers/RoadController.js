

app.controller('RoadController', function($scope, $http, $location, AccommodationService, AdvanceService) {

            $scope.showTheForm=true;
            $scope.ShowMessage=false;

            $http.get("/travel/list/")
                .success(function(response) {$scope.names = response;});

            $http.get("/travel/listadv/")
                .success(function(response) {$scope.adv = response;});

            $scope.processForm = function(postdetails) {
                  $http({
                  method  : 'POST',
                  url     : '/travel/roadadd/',
                  data    : $.param({
                            departure_location: $scope.departure_location,
                            destination_location: $scope.destination_location,
                            mileage: $scope.mileage,
                            departure_date: $scope.departure_date,
                            accommodation: $scope.accommodations,
                            advance:$scope.advances,
                            mileage_cost:$scope.mileage_cost,
                            postdetails:$scope.postdetails,
                            advance_len:$scope.advances.length,
                            accommodation_len:$scope.accommodations.length

                  }),  // pass in data as strings
                  headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
                 })
                  .success(function(data) {
                    //console.log(data);
                      $scope.showTheForm=false;
                      $scope.ShowMessage=true;
                      //$location.path('/travel/test/');
                  });
                };

            $scope.departure_location = "";
            $scope.destination_location = "";
            $scope.mileage = "";
            $scope.departure_date = "";

            $scope.postdetails = postdetails;
            $scope.purpose = purpose;
            $scope.accomodation_cost = accomodation_cost;

            $scope.mileage_cost = $scope.mileage * 50;
            $scope.accommodations = AccommodationService.accommodations;
            $scope.total = $scope.getTotal * $scope.mileage_cost;

            $scope.getTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                for(var i = 0; i < $scope.accommodations.length; i++){
                    console.log('ft' + $scope.accommodations[i].diff)
                    var diff = $scope.accommodations[i].diff;
                    total += (diff * $scope.accomodation_cost);
                }
                return total;
            }

             $scope.addAccommodation = function() {
                $scope.newAccommodation.diff = diffDate($scope.newAccommodation.check_out_date, $scope.newAccommodation.check_in_date);
                AccommodationService.accommodations.push($scope.newAccommodation);
                $scope.newAccommodation = {};
              }

             $scope.deleteAccommodation = function(accommodation)
              {
                 AccommodationService.accommodations.pop(accommodation);
                 console.log("Delete " + accommodation)
              }

            $scope.getTotal = function(){
                var total = 0;
                console.log('check total' + $scope.accommodations.length)
                for(var i = 0; i < $scope.accommodations.length; i++){
                    console.log('ft' + $scope.accommodations[i].diff)
                    var diff = $scope.accommodations[i].diff;
                    total += (diff * $scope.accomodation_cost);
                }
                return total;
            }

            $scope.advances = AdvanceService.advances;
            $scope.addAdvance = function(){
                $scope.newAdvance.cost = $scope.newAdvance.units * $scope.newAdvance.rate;
                        console.log($scope.newAdvance)
                        AdvanceService.advances.push($scope.newAdvance);
                        $scope.newAdvance = {};
                      }

                $scope.deleteAdvance = function(advance){
                     AdvanceService.advances.pop(advance)
                     console.log("Delete Advance" + advance )
                }



         });