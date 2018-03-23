classdef mdpNodeAdvanced < mdpNode
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Defines a basic MDP learning node with no messaging.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
    properties
        Message;
        TxMessage;          % determines whether node sends messages or not
        MessagePeriod;      % time between messages
        
        R;      % reward matrix
        R_count;% counting matrix for rewards 
    end
    
    methods
        
         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Constructor
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function obj = mdpNodeAdvanced(numChans,states,numSteps)
            obj@mdpNode(numChans,states,numSteps);
            
            obj.Message = nodeMessage('default',0, 100);
            obj.TxMessage = 0;          % determines whether node sends messages or not
            obj.MessagePeriod = 2000;   % time between messages
            obj.R = zeros(obj.numStates,obj.numActions);
            obj.R_count = zeros(obj.numStates,obj.numActions);
            
        end
        
        function CreateMessage(node,MessageType, MessageBand)
                node.Message.SetType(MessageType);
                node.Message.SetBand(MessageBand);
        end
        
        function tmp = ReceiveMessage(node,message)
            if message.MessageType == 'RequestBand'
                node.R(:,message.band+1) = node.R(:,message.band+1) - message.BandAvoidPenalty;
            else
                error('Message Type misdefined.');
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
                [~,indC] = ismember(obj.actionHist(stepNum-1,:),obj.actions,'rows');
                
                obj.stateTrans(indA,indB,indC) = obj.stateTrans(indA,indB,indC) + 1;
                obj.rewardTrans(indA,indB,indC) = obj.rewardTrans(indA,indB,indC) + obj.rewardHist(stepNum-1);
                
                obj.R_count(indA,indC) = obj.R_count(indA,indC) + 1;
                obj.R(indA,indC) = (obj.R_count(indA,indC)-1)*obj.R(indA,indC)/obj.R_count(indA,indC) + obj.rewardHist(stepNum-1)/obj.R_count(indA,indC);
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
            
            [~,obj.policy] = mdp_policy_iteration(obj.avgStateTrans,obj.R,obj.discountFactor);
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
                otherwise
                    error('exploreDecayType misdefined');
            end
            obj.exploreHist = [obj.exploreHist, obj.exploreProb];
        end

        
    end
    
end