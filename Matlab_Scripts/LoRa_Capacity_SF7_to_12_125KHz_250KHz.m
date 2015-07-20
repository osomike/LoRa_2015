clear;
clc;

%% Initialization 
sf = [7:1:12];      % Spreading factor range
pl = [16:10:256];   % Payload size in bytes (MAC Payload)

[SF,PL] = meshgrid(sf,pl);
SF_sf7_bw250 = 6*ones(length(pl),1); % for SF7 and 250KHz of bandwidth (we use '6' just for plotting)
PL_sf7_bw250 = PL(:,1); % for SF7 and 250KHz of bandwidth

%% VARIABLES
codingRate = 1; % Coding rate values 4/(CR+4) | 1->4/5 | 2->4/6 | 3->4/7 | 4->4/8
bw = 125;       % Used bandwidth in KHz
nPreamble = 8;  % Preamble length in symbols
maxPercentageOnAir = 0.1/100; %Maximum percentage of channel using <0.1%
maxPacketsSentDaily = 24; % Maximum number of packets sent daily per LoRaMote
totalNumberChannels = 10; % CH0 - CH9 ?

%% Symbol rate and Symbol Period calculation
symRate_s   = 'bw*1000/(2^SF)';             % Symbol rate calculation
symRate     = eval(vectorize(symRate_s));   
symPeriod   = 1./symRate;                   % Symbol period calculation

symPeriod_sf7_bw250 = 1/(250*1000/(2^7));   % Symbol period for a SF7 and 250KHz configuration
symPeriod_sf7_bw250 = symPeriod_sf7_bw250*ones(length(pl),1); % Array to concatenate then

%% Preamble length and preamble duration calculation
totalPreambleLength = (4.25 + nPreamble);           % Total preamble length in symbols

%% Packet length and packet duration calculation
% For more details refer to the sx1272 DataSheet document (4.1.1.7. "Time on air", pag 29)
boolFixedLength = 0;    % Boolean variable to use or not a fixed length (implicit or explicit header)
boolOptimization = 1;   % Boolean variable to use or not an optimization
boolCRC = 1;            % Boolean variable to use or not CRC
tmp_s = '(8*PL - 4*SF + 28 - 16*boolCRC - 20*boolFixedLength)*(codingRate + 4)/(4*(SF-2*boolOptimization))';
tmp = eval(vectorize(tmp_s));

totalPayloadLength = 8 + max(ceil(tmp) ,0);
totalPayloadLength_sf7_bw250 = totalPayloadLength(:,1); % Results for SF7 and 250KHz configuration (same as SF7 @ 125KHz)

totalPayloadLength = [totalPayloadLength_sf7_bw250 totalPayloadLength];  % Concatenation for both results

symPeriod_total = [symPeriod_sf7_bw250 symPeriod];  % Concatenation for both Symbol periods (@ 125KHz & 250KHz)

onAirTime = (totalPreambleLength + totalPayloadLength).*symPeriod_total; % Packet duration calculation

%% Calculation of maximum number of packets to send daily per end-device
% Considering the maximum channel occupation (0.1%) we perform 
% the calculations to get the maximum available number of packets
% send daily
maxTotalPackets = 24*3600./(onAirTime/maxPercentageOnAir);

%% Calculation of maximum number end-devices
% Considering the channel occupation we perform the calculations
% to get the maximum possible number of end-devices 
maxPossibleLoRaDevices = totalNumberChannels*24*3600./(onAirTime*maxPacketsSentDaily);



%% Plotting resutls :p
SF = [SF_sf7_bw250 SF];  % Dimmension adjustement
PL = [PL_sf7_bw250 PL];  % Dimmension adjustement 

figure
rotate3d on
surfc(SF,PL,maxTotalPackets)
title('Maximum number of packets for LoRa Modulation')
xlabel('Spreading factor SF')
ylabel('Payload Size Bytes')
zlabel('Daily maximum number of packets per channel per end-device')
axis tight
%shading interp
colorbar
MyBox = uicontrol('style','text');
set(MyBox,'Position',[0,0,150,50]);
set(MyBox,'String','Consider that a SF7 with 250KHz of bandwidth is represented by "SF6" ');

figure
rotate3d on
surfc(SF,PL,maxPossibleLoRaDevices)
title('Maximum number of simultaneous LoRa devices considering 10 available channels')
xlabel('Spreading factor SF')
ylabel('Payload Size Bytes')
zlabel('Maximum simultaneous LoRa end-devices')
axis tight
%shading interp
colorbar
MyBox = uicontrol('style','text');
set(MyBox,'Position',[0,0,150,50]);
set(MyBox,'String','Consider that a SF7 with 250KHz of bandwidth is represented by "SF6" ');