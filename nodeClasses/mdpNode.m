classdef mdpNode < radioNode
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Defines a basic MDP learning node with no messaging.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    properties
        goodChans
        
        numStates
        states
        stateHist
        stateTally
        stateTrans
        avgStateTrans
        
        discountFactor = 0.9
        policyAdjustRate = 100         % Policy is adjusted at this step increment
        
        exploreProb                     % Current exploration probability
        exploreInit = 1.0               % Initial exploration probability
        exploreDecay = 0.1              % Percentage reduction in exploration chance per policy calculation
        exploreHist
        
        exploreDecayType = 'perf';             % either 'expo', 'step' or 'perf'
        exploreWindow = 500;           % only used with 'step'
        exploreMin = 0.01;              % only used with 'step'
        
        explorePerf = 10;               % only used with 'perf' 
        explorePerfWin = 100;           % triggers jump in explore prob to
                                        % 1 if reward is below this over 
                                        % last explorePerfWin epochs
        
        policy
        policyHist        
        % [Not transmitting, Good Channel no Interference, Good Channel Interference, Bad Channel no Interference, Bad Channel Interference]
        rewards = [-200, 100, -100, 50, -200];
        
        rewardHist
        rewardTally        
        rewardTrans
        cumulativeReward
    end
    
    methods
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Constructor
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function obj = mdpNode(numChans,states,numSteps)
            obj.actions = zeros(numChans+1,numChans);
            for k = 1:numChans
                obj.actions(k+1,k) = 1;
            end
            obj.numActions = size(obj.actions,1);  
            obj.actionTally = zeros(1,numChans+1);
            obj.actionHist = zeros(numSteps,numChans);
            obj.actionHistInd = zeros(1,numSteps);
            
            obj.goodChans = ones(1,numChans);
            
            obj.states = states;
            obj.numStates = size(states,1);
            
            obj.stateHist = zeros(numSteps,numChans);
            obj.stateTally = zeros(1,obj.numStates);
            obj.stateTrans = zeros(obj.numStates,obj.numStates,obj.numActions);
            obj.stateTrans(:,1,:) = ones(obj.numStates,1,obj.numActions);
            obj.avgStateTrans = zeros(obj.numStates,obj.numStates,obj.numActions);
            
            obj.rewardHist = zeros(1,numSteps);
            obj.rewardTally = zeros(1,numChans+1);
            obj.cumulativeReward = zeros(1,numSteps);
            obj.rewardTrans = zeros(obj.numStates,obj.numStates,obj.numActions); 
            
            obj.exploreProb = obj.exploreInit;
            obj.exploreHist = obj.exploreProb;
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Determines an action from the node's possible actions
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function action = getAction(obj,stepNum)
            if rand < obj.exploreProb
                action = obj.actions(randi(obj.numActions),:);
            else
                [~,stateIndex] = ismember(obj.stateHist(stepNum-1,:),obj.states,'rows');
                action = obj.actions(obj.policy(stateIndex),:);
            end
            
            obj.actionHist(stepNum,:) = action;
                        
            if ~sum(action)
                obj.actionTally(1) = obj.actionTally(1) + 1;
                obj.actionHistInd(stepNum) = 1;
            else
                obj.actionHistInd(stepNum) = find(action == 1) + 1;
                obj.actionTally(2:end) = obj.actionTally(2:end) + action;           
            end
        end 
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Determines the reward earned from action based on if a good
        % channel was used and if there was a colission.
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function getReward(obj,collision,stepNum)
            action = obj.actionHist(stepNum,:);

            if ~sum(action)
                reward = obj.rewards(1);
                obj.rewardTally(1) = obj.rewardTally(1) + reward;
            else
                if isempty(find(obj.goodChans+action > 1, 1))
                    if collision == 1
                        reward = obj.rewards(5);
                    else
                        reward = obj.rewards(4);
                    end
                else
                    if collision == 1
                        reward = obj.rewards(3);
                    else
                        reward = obj.rewards(2);
                    end
                end                             
                obj.rewardTally(2:end) = obj.rewardTally(2:end) + action*reward;
            end
            obj.rewardHist(stepNum) = reward;   
            
            if stepNum == 1
                obj.cumulativeReward(stepNum) = reward;
            else
                obj.cumulativeReward(stepNum) = obj.cumulativeReward(stepNum-1) + reward;
            end
        end  
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Updates the state and reward transition matrices.
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function updateTrans(obj,observedState,stepNum)
            obj.stateHist(stepNum,:) = observedState;
            
            [~,indB] = ismember(obj.stateHist(stepNum,:),obj.states,'rows');
            obj.stateTally(indB) = obj.stateTally(indB) + 1;
            
            if stepNum > 1
                [~,indA] = ismember(obj.stateHist(stepNum-1,:),obj.states,'rows');
                [~,indC] = ismember(obj.actionHist(stepNum,:),obj.actions,'rows');
                
                obj.stateTrans(indA,indB,indC) = obj.stateTrans(indA,indB,indC) + 1;
                obj.rewardTrans(indA,indB,indC) = obj.rewardHist(stepNum);
            end
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Update the node's policy.
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function updatePolicy(obj,step)
            obj.avgStateTrans = obj.stateTrans;
            for k = 1:obj.numStates
                for kk = 1:obj.numActions
                    obj.avgStateTrans(k,:,kk) = obj.avgStateTrans(k,:,kk) / sum(obj.avgStateTrans(k,:,kk));                    
                end
            end
            obj.avgStateTrans(isnan(obj.avgStateTrans)) = 0;
            
            [~,obj.policy] = mdp_policy_iteration(obj.avgStateTrans,obj.rewardTrans,obj.discountFactor);
            obj.policy = obj.policy.';
            
            obj.policyHist = [obj.policyHist; obj.policy];
            
            switch obj.exploreDecayType
                case 'expo'
                    obj.exploreProb = obj.exploreInit*exp(-obj.exploreDecay*size(obj.policyHist,1));     
                case 'step'
                    if step > obj.exploreWindow
                        obj.exploreProb = obj.exploreMin;
                    else
                        obj.exploreProb = 1;
                    end
                case 'perf'
                     obj.exploreProb = obj.exploreInit*exp(-obj.exploreDecay*size(obj.policyHist,1));     
                     if (mean(obj.rewardHist(step-obj.explorePerfWin+1:step)) < obj.explorePerf) & (obj.exploreProb < 0.05)
                         obj.exploreProb = 0.2; %obj.exploreProb + obj.explorePerfJump;
                     end
                otherwise
                    error('exploreDecayType misdefined');
            end
            obj.exploreHist = [obj.exploreHist, obj.exploreProb];
        end
    end   
end

