(function() {

    var onBoardingController = function($scope) {

        $scope.Accomodation = [];
        $scop.roadTravl =[];



        $scope.addKitTag = function (kyckittag) {
            if (kyckittag != null) {
                $scope.kycKitTags.push(kyckittag);
                $scope.kyckittag = "";
                console.log("add kit tag : " + $scope.kycKitTags.length);
            }
        }

        $scope.deleteKitTag = function(kyckittag) {
            $scope.kycKitTags.pop(kyckittag);
            console.log("add kit tag : " + $scope.kycKitTags.length);
        }


        $scope.$inject = ["$scope"];
    };

    asmd.controller("onBoardingController", onBoardingController);
})();

