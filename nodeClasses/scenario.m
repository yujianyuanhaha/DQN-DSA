classdef scenario < handle    % derive, not less or equal
    
    
    % simulationScenario = scenario(numSteps,'fixed',3);  example
  
    properties     
        numSteps;
        scenarioType;  % 'ncorn' or 'fixed'
        numIntervals;
        intervalSize;
    end
    
    methods
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Constructor
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function obj = scenario(numSteps,scenarioType,numIntervals)
            
            obj.numSteps = numSteps;
            obj.numIntervals = numIntervals;
            obj.scenarioType = scenarioType;
            obj.intervalSize = numSteps/numIntervals;   % redundency 
            
            
            
        end
        
        function initializeScenario(obj,nodes,indicies)
        
            numNodes = length(indicies);    % index
            for i=1:numNodes
                nodes{indicies(i)}.txProbability = 0;
            end
       
            
        end
        
        function updateScenario(obj,nodes, indicies, steptime)
            
            numNodes = length(indicies);
            
            switch obj.scenarioType
                
                case 'ncorn'
               
                    currentInterval = floor(steptime/obj.intervalSize);
                    if steptime > obj.numSteps*(obj.numIntervals-1)/obj.numIntervals
                        currentInterval = obj.numIntervals;
                    end
                    
                    
                     for i=1:numNodes
                        nodes{indicies(i)}.txProbability = currentInterval/obj.numIntervals;        % -j ??                       
                     end
                    
                     
                     
                     
                case 'fixed'    % nothing in fixed
                    
                otherwise 
                    error('scenario.Type is unknown');
            end
            
        end
        
        

    end  
end