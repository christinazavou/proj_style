% pre-select patches
function []=run_cluster(views,K,HOG_Path,cluster_Path)
    fprintf('start run cluster\n');
    if ~exist(cluster_Path,'dir')
        mkdir(cluster_Path);
    end

    for viewsi=1:views
        vdatapath=fullfile(cluster_Path,sprintf('kmeans-%d-%d.mat',K,viewsi));
        if isfile(vdatapath)
            continue;
        vcurpath=fullfile(HOG_Path,sprintf('V-%d.mat',viewsi));
        load(vcurpath);
        % idxk keeps the cluster index for each of the V rows (i.e. each hog-patch-feature), 
        % ceter keeps the 50 clusters (i.e. has size 50x900)
        [idxk,ceter]=kmeans(V,K,'emptyaction','drop');
        pos=find(isnan(ceter(:,1)));
        newceter=ceter;
        for i=1:length(pos)       
            newceter(pos(i),:)=0;
        end
        save(vdatapath,'idxk','ceter','pos','newceter');
        fprintf('%d\n', viewsi);
    end
    fprintf('finish run cluster\n');
end