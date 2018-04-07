classdef nodeMessage < handle

    properties     
        band
        MessageType          % 'RequestBand', 'ReleaseBand'
        BandAvoidPenalty
    end
    
    methods
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Constructor
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        function obj = nodeMessage(message_type, band, band_avoid_pen)
            obj.MessageType = message_type;
            obj.band = band;
            obj.BandAvoidPenalty = band_avoid_pen;
        end
        
        function SetType(obj, message_type)
            obj.MessageType = message_type;
        end
        
        function SetBand(obj, band)
            obj.band = band;
        end

    end  
end