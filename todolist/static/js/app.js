
var app = angular.module('app', ['ngRoute','ngCookies']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  });

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

app.run( function run( $http, $cookies ){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
    alert($cookies.getAll())
})



app.config(function($routeProvider, $locationProvider) {
  $routeProvider
   .when('/:planName', {
        templateUrl: '/static/templates/task_list.html',
        controller: 'TaskService',
     })
   .otherwise({
        templateUrl: '/static/templates/mylists.html',
        controller: 'PlanListController',
     });
     
});
app.factory('Exibitplan', function() {
    function ExibitMarkSelect(plan) { 
        this.plan = plan;
        var _self = this;
       
        this.markOffAll = function() {
            for(task in _self.plan.tasks) {
                
              _self.plan.tasks[task].activate = false;
            }
        }
        _self.markOffAll();
        this.markItem = function(task){ 
            _self.markOffAll();
            task.activate = true;
        }
    }

    return {
        createNew: function(plan) {
            return new ExibitMarkSelect(plan);
        }
    };
});
app.controller('TaskService', function($http,$scope,$routeParams,Exibitplan){  
    var exibit ;
    $scope.currentTask = "";
    $scope.modEdit = false;
    $http.get('api/plan/'+$routeParams.planName)
    .success(function(data) {
        exibit = Exibitplan.createNew(data);
        $scope.plan = exibit.plan;
    })
  
    $scope.adicionarTask = function(plan){
        $http.post('api/task', {"name":plan.newTask,"plan":plan.id})
        .success(function(data) {
          plan.tasks.push(data)
            plan.newTask = null;
        })
    }       
    
    $scope.selectTask = function(task){
       exibit.markItem(task);
       $scope.currentTask = task.name;
    }
    
    $scope.removerTask = function(task,tasks){
        $http.delete('api/task/'+task.id)
        .success(function(data) {
        var index = tasks.indexOf(task);
            if (index != -1) {
                tasks.splice(index, 1);
            }
        })
    }
    $scope.alterTask = function(task,text){
        $http.patch('api/task/'+task.id, {"description":text})
        .success(function(data) {
            task.description = text;
            $scope.modEdit = false;
        })
    } 
});

app.controller('PlanListController', function ($scope, $http) {
    
  if ($scope.plans === undefined) {
  $http.get('api/plans')
      .success(function(data) {
     	   $scope.plans = data;
   	})
  }
  
  $scope.adicionarPlan = function(){
        $http.post('api/plans', {"name":$scope.newPlan,"tasks":[]})
   	    .success(function(data) {
     	    $scope.plans.push(data)
   	        $scope.newPlan = null;
         })
      }
    
   $scope.removerPlan = function(plan){
       $http.delete('api/'+plan.id)
   	    .success(function(data) {
     		var index = $scope.plans.indexOf(plan);
            if (index != -1) {
                $scope.plans.splice(index, 1);
               
            }
        })
    }
});

