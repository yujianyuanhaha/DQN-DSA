classdef dsaNode < legacyNode
    % one typical of 'legacy Node'
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Defines a node with the default behavior of always using the same
    % randomly chosen channel.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    properties
        observedState;
        stateHist;
    end
    
    methods
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Constructor
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function obj = dsaNode(numChans,numSteps,txProb)
            obj@legacyNode(numChans,numSteps,txProb)    % @ magic 
            % https://www.mathworks.com/help/matlab/matlab_oop/calling-superclass-methods-on-subclass-objects.html
            % subclass superclass
            
            obj.actions = zeros(numChans+1,numChans);
            for k = 1:numChans
                obj.actions(k+1,k) = 1;
            end                                % similiar to hopping as well
            obj.numActions = size(obj.actions,1); 
            obj.actionTally = zeros(1,numChans+1);
            obj.actionHist = zeros(numSteps,numChans);
            obj.actionHistInd = zeros(1,numSteps);
            obj.txProbability = txProb;
            obj.observedState = zeros(1,numChans);
            obj.stateHist = zeros(numSteps+1,numChans);
        end    
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Determines an action from the node's possible actions
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function action = getAction(obj,stepNum)
            
            ind = find(obj.observedState == 0);
            %ind = ind(randi(length(ind)));
            
            if stepNum > 1
                if find(obj.actionHistInd(stepNum-1) == ind+1)
                    ind = obj.actionHistInd(stepNum-1)-1;
                else
                    ind = ind(randi(length(ind)));
                end
            else
                ind = ind(randi(length(ind)));
            end
            
            if rand <= obj.txProbability
                action = obj.actions(ind+1,:);   %  obj.actions = zeros(numChans+1,numChans);
            else
                action = zeros(1,size(obj.actions,2));
            end
            
            % conclusion: occupy one once see a empty one, greedy
            
            obj.actionHist(stepNum,:) = action;
            if ~sum(action)
                obj.actionHistInd(stepNum) = 0;
            else
                obj.actionHistInd(stepNum) = find(action == 1) + 1;
            end
            
            if ~sum(action)
                obj.actionTally(1) = obj.actionTally(1) + 1;
            else
                obj.actionTally(2:end) = obj.actionTally(2:end) + action;
            end
        end
        
        function updateState(obj,observedState,s)
            obj.observedState = observedState;
            obj.stateHist(s+1,:) = observedState;
        end
        
    end
end