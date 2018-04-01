classdef legacyNode < radioNode     % most basic one
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Defines a node with the default behavior of always using the same
    % randomly chosen channel.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    properties
    end
    
    methods
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Constructor
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function obj = legacyNode(numChans,numSteps,txProb)   % notice probabilty, tx after choose
            obj.actions = zeros(1,numChans);
            obj.actions(randi(numChans)) = 1;   % X = randi(imax) returns a pseudorandom scalar integer between 1 and imax.
            obj.numActions = size(obj.actions,1); 
            obj.actionTally = zeros(1,numChans+1);
            obj.actionHist = zeros(numSteps,numChans);
            obj.actionHistInd = zeros(1,numSteps);
            obj.txProbability = txProb;
        end    
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Determines an action from the node's possible actions
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function action = getAction(obj,stepNum)
            
            if rand <= obj.txProbability
                action = obj.actions;   %  obj.actions = zeros(1,numChans);
            else
                action = zeros(1,length(obj.actions));
            end
            
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
    end
end