%% Script Initializations
close all; clear; clc; tic;
warning('off', 'MATLAB:singularMatrix')  % -j warning()
warning('off', 'MATLAB:illConditionedMatrix')
addpath('mdpToolbox');
addpath('nodeClasses');

%% Simulation Parameters
numSteps = 30000/3;                    % Simulation steps per iteration
numChans = 4;                        % Number of frequency channels available
nodeTypes = [2,1,1,0];               % The type of each node
                                       % 0 - Legacy (Dumb) Node
                                       % 1 - Hopping Node
                                       % 2 - MDP Node
                                       % 3 - DSA node (just avoids)          %% -j mechanism of DSA tag as TODO   
                                       % 4 - Adv. MDP Node
legacyTxProb = 1;                                   
numNodes = length(nodeTypes);        % Number of nodes

hiddenNodes = [0,0,0,0];     % should be length numNodes 
                                           % 1--> hidden, 0 --> not hidden (default)
exposedNodes = [0,0,0,0];    % should be length numNodes                              
                                           % 1--> exposed, 0 --> not exposed (default)
                             % -j no collision, no hidden so far, if exist, there exist choice 'no transmit' 
                             % NEXT STEP, deal with hidden node
                                
if length(hiddenNodes) < numNodes
   hiddenNodes = [hiddenNodes,zeros(1,NumNodes-length(hiddenNodes))];       % padding with zero
end 

%% Initializing Nodes, Observable States, and Possible Actions
states = stateSpaceCreate(numChans);
numStates = size(states,1);    % -j size(,1);  % return the first dim

nodes = cell(1,numNodes);   % cell array, abtrary data structure
for k = 1:numNodes
    if nodeTypes(k) == 0
        nodes{k} = legacyNode(numChans,numSteps,legacyTxProb);  % function return a handle with name 'legacyNode'
    elseif nodeTypes(k) == 1
        nodes{k} = hoppingNode(numChans,numSteps);
    elseif nodeTypes(k) == 2
        nodes{k} = mdpNode(numChans,states,numSteps);
    elseif nodeTypes(k) == 3
        nodes{k} = dsaNode(numChans,numSteps,legacyTxProb);        %% note dsa legacyTxProb
    elseif nodeTypes(k) == 4
        nodes{k} = mdpNodeAdvanced(numChans,states,numSteps);
    end      
    
    nodes{k}.hidden = hiddenNodes(k);
    nodes{k}.exposed = exposedNodes(k);    
end
clear k

% nodes{1}.goodChans = [1,1,0,0];
% nodes{2}.goodChans = [0,1,1,0];
% nodes{3}.goodChans = [0,0,1,1];   % comment out

simulationScenario = scenario(numSteps,'fixed',3);  % 'fixed' or 'ncorn'


%% Vector and Matrix Initializations
actions = zeros(numNodes,numChans);
collisions = zeros(1,numNodes);
collisionTally = zeros(numNodes);
collisionHist = zeros(numSteps,numNodes);
cumulativeCollisions = zeros(numSteps,numNodes);    

%% Main Loops
toc
disp('Starting Main Loop');             % display on terminal
%nodes{1}.CreateMessage('RequestBand',4);
%nodes{2}.CreateMessage('RequestBand',1);
%nodes{3}.CreateMessage('RequestBand',3);
%nodes{4}.CreateMessage('RequestBand',2);

legacyNodeIndicies = [];
for n = 1:numNodes
   if (isa(nodes{n},'legacyNode'))          % -j isa() Determine if input is object of specified class
        legacyNodeIndicies = [legacyNodeIndicies,n];
   end
end

if ((simulationScenario.scenarioType ~= 'fixed') & ~isempty(legacyNodeIndicies))
    simulationScenario.initializeScenario(nodes,legacyNodeIndicies);
end

for s = 1:numSteps
    
    % Determination of next action for each node
    for n = 1:numNodes
            actions(n,:) = nodes{n}.getAction(s);           % -J key 1 _Node.getAction
    end
    
    if (simulationScenario.scenarioType ~= 'fixed')
            simulationScenario.updateScenario(nodes,legacyNodeIndicies, s);   % what is update for, next time slots?
    end
    
    
    % Determining observations, collisions, rewards, and policies (where applicable)
    observedStates = zeros(numNodes,numChans);
    for n = 1:numNodes
        collisions(n) = 0;

        for nn = 1:numNodes   % nest loop
            if n ~= nn
                if ~(nodes{nn}.hidden)
                    observedStates(n,:) = (observedStates(n,:) + actions(nn,:) > 0);  
                    % what is the eaxct definition - states update after other nodes actions
                    % global full observe
                end
                if (sum(actions(n,:)) > 0) && (~isempty(find((actions(n,:) + actions(nn,:)) > 1, 1))) && ~nodes{nn}.exposed
                        collisions(n) = 1;
                        collisionTally(n,nn) = collisionTally(n,nn) + 1;
                        % draft
                        % find(    (actions(n,:) + actions(nn,:)) > 1, 1    )
                end
            end
        end
        
        if isa(nodes{n},'mdpNode')
            nodes{n}.getReward(collisions(n),s);    % should replace damn s -> t for timestamp
            nodes{n}.updateTrans(observedStates(n,:),s);      % input for update the trans
            
            if ~mod(s,nodes{n}.policyAdjustRate)   % mod() - Remainder after division (modulo operation)
                nodes{n}.updatePolicy(s);
            end
        end
        
        if isa(nodes{n},'mdpNodeAdvanced')
            if nodes{n}.TxMessage && (floor(s/nodes{n}.MessagePeriod) == s/nodes{n}.MessagePeriod)
                for nn=1:numNodes
                    if nn ~= n
                        nodes{nn}.ReceiveMessage(nodes{n}.Message);
                    end
                end
            end
        end    % temporal leave it alone
        
        if isa(nodes{n},'dsaNode')
            nodes{n}.updateState(observedStates(n,:),s)
        end
        
    end
    
    collisionHist(s,:) = collisions;
    cumulativeCollisions(s,:) = collisions;
    if s ~= 1
        cumulativeCollisions(s,:) = cumulativeCollisions(s,:) + cumulativeCollisions(s-1,:);
    end
    
    
    
end
clear s n actions nn collisions observedStates
fprintf('Ending Main Loop After %0.2f seconds.\n',toc);





%% ***************************************************************
%% Outputs and Plotting
figure(1); hold on;  %  cumulativeCollisions
for n = 1:numNodes
    plot(cumulativeCollisions(:,n));      
    if isa(nodes{n},'dsaNode')
        legendInfo{n} = sprintf('Node %d (DSA)',n);   
    elseif isa(nodes{n},'hoppingNode')
        legendInfo{n} = sprintf('Node %d (Hopping)',n);
    elseif isa(nodes{n},'mdpNode')
        legendInfo{n} = sprintf('Node %d (MDP)',n);
    elseif isa(nodes{n},'legacyNode')
        legendInfo{n} = sprintf('Node %d (Legacy)',n);
    end
    
    txPackets(:,n) = [cumsum(  sum(nodes{n}.actionHist' )')   ];
    
end
legend(legendInfo,'Location','northwest');
xlabel('Step Number');
ylabel('Cumulative Collisions');
title('Cumulative Collisions Per Node');
clear k legendInfo

figure(2); hold on;
c = 1;
for n = 1:numNodes
    if isa(nodes{n},'mdpNode')
        plot(nodes{n}.cumulativeReward)     % .cumulativeReward
        legendInfo{c} = sprintf('Node %d (MDP)',n);
        c = c + 1;
    end
end
if exist('legendInfo','var')
    legend(legendInfo,'Location','northwest');
    xlabel('Step Number');
    ylabel('Cumulative Reward');
    title('Cumulative Reward Per Learning Node');
end
clear c n legendInfo

figure(3)   % notice the trick plot Fig3
split = ceil(numNodes / 2);
for n = 1:numNodes
    if n <= split
        subplot(split,2,n); 
    else
        subplot(split,2,n);
    end
    
    if isa(nodes{n},'mdpNode')
        offset = 1;
    else
        offset = 0;
    end
    plot( max(nodes{n}.actionHistInd-1 , zeros(1,numSteps)),'bo')       %actionHistInd
    ylim([0,numChans+2]);
    xlabel('Step Number');
    ylabel('Action Number');
    
    if isa(nodes{n},'legacyNode')
        title(sprintf('Action Taken by Node %d (Legacy)',n));
    elseif isa(nodes{n},'hoppingNode')
        title(sprintf('Action Taken by Node %d (Hopping)',n));
    elseif isa(nodes{n},'mdpNode')
        title(sprintf('Action Taken by Node %d (MDP)',n));
    end
    if isa(nodes{n},'dsaNode')
        title(sprintf('Action Taken by Node %d (DSA)',n));
    end
end
clear n legendInfo

%% Simulation Cleanup
simulationParams.numSteps = numSteps;
simulationParams.numChans = numChans;
simulationParams.numNodes = numNodes;
simulationParams.nodeTypes = nodeTypes;
simulationParams.states = states;
simulationParams.numStates = numStates;
timeSlots = repmat([1:numSteps]',1,numNodes);

results.collisionTally = collisionTally;    % first appear 'results', define 'structure' in matlab
results.collisionHist = collisionHist;
results.cumulativeCollisions = cumulativeCollisions;
results.PER = results.cumulativeCollisions./txPackets;
results.PLR = (results.cumulativeCollisions+(timeSlots-txPackets))./timeSlots;
%clear collisionTally collisionHist cumulativeCollisions

figure
c = 1;
for i=1:numNodes
        if isa(nodes{i},'mdpNode')
            semilogy(results.PER(:,i))                  % (results.PER(:,i)
            legendInfo{c} = sprintf('Node %d (MDP)',i);
        elseif isa(nodes{i},'dsaNode')
            semilogy(results.PER(:,i))
            legendInfo{c} = sprintf('Node %d (DSA)',i);
        elseif isa(nodes{i},'legacyNode')
            semilogy(results.PER(:,i))
            legendInfo{c} = sprintf('Node %d (legacy)',i);
        end
        c = c + 1;
        hold on

 end
xlabel('Step Number')
ylabel('Cumulative Packet Error Rate')
legend(legendInfo)

figure
c = 1;
clear legendInfo;
for i=1:numNodes
        if isa(nodes{i},'mdpNode')              % results.PLR(
            semilogy(results.PLR(:,i))
            legendInfo{c} = sprintf('Node %d (MDP)',i);
       end
        c = c + 1;
        hold on

end
if exist('legendInfo','var')
    xlabel('Step Number')
    ylabel('Cumulative Packet Loss Rate')
    legend(legendInfo)
end

%clear numSteps numChans numNodes nodeTypes states numStates

% fully understand code is a must
% however, prority, get the codes running first.





