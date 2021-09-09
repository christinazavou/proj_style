% output kernel for convoluting
function []=run_cluster_idf(views,kernel_Path,HOG_Path,cluster_Path,patch_Path,models,sample_size,K)
    fprintf('start run cluster idf\n');
    if ~exist(kernel_Path,'dir')
        mkdir(kernel_Path);
    end

    %% 
    for viewi=1:views
        vcurpath=fullfile(HOG_Path,sprintf('V-%d.mat',viewi));
        load(vcurpath);
        kcurpath=fullfile(cluster_Path,sprintf('kmeans-%d-%d.mat',K,viewi));
        load(kcurpath);
        curpath=fullfile(patch_Path,num2str(viewi));
        %find the closest patch to be kernel
        patchk=zeros(K,1);  % keeps the index of the patch that lies closer to each cluster
        disk=1./patchk;  % keeps the closest distance from a patch for each cluster
        [V_length,unused] = size(V); 
        for ni=1:V_length
            % idkx is from "run_cluster" and contains the cluster id of each patch in V
            % so oi is the cluster of current patch
            oi=idxk(ni,1);
            % newceter is from "run_cluster" and contains the (k-means) clusters' centers
            % so dis is the distance of the current patch from the cluster center it belongs to
            dis=sum((newceter(oi,:)-V(ni,:)).^2);
            if(dis<disk(oi,1))
                patchk(oi,1)=ni;
                disk(oi,1)=dis;
            end
        end

        fprintf('writing kernel images\n');
        impathk=fullfile(kernel_Path,num2str(viewi));
        if ~exist(impathk,'dir')  
            mkdir(impathk,'dir')
        end
        fk2p=fopen(fullfile(impathk,'k2po.txt'),'w');
        fidai=fopen(fullfile(impathk,'Apidfpatchname.txt'),'w');
        count=0;
        cnt=0;
        patchkernel=[];
        % loop over all patches using the count as the patch idx (does not increment if patch doesnt exist)
        % and if a patch represents a cluster then store the information
        % patchkernel keeps the cluster id of each patch that represents a cluster (i.e. its size is 50, 1)
        % for each kernel we store the patch that represents it? :/
        for nm=1:models
            for nmi=1:sample_size
                patchname = sprintf('%d_%d.bmp',nm,nmi);
                imPathksoure=fullfile(curpath,patchname);
                 if ~exist(imPathksoure,'file')
                     continue;
                 end
                count = count+1;
                pos=find(patchk==count);
                if ~isempty(pos)
                     imPathkn=fullfile(impathk,patchname);
                     pic=imread(imPathksoure);
                     imwrite(pic, imPathkn, 'bmp'); 
                     cnt=cnt+1;
                     patchkernel(cnt,1)=idxk(count,1);
                     fprintf(fidai,'%s\r\n', patchname);
                     fprintf(fk2p,'%d\r\n', patchkernel(cnt,1));
                end

            end
        end     
        fclose(fidai);
        fclose(fk2p);

        %%
        fprintf('calculating kernel model\n');
        count1=0;
        % kernelModel is a matrix for each view, with size [num_clusters, num_models]
        % it stores how many times each cluster appears in each model
        kernelModel{viewi,1}=ones(length(patchkernel),models)*-1;
        for nn=1:models
            for nni=1:sample_size
                patchnamepath=fullfile(curpath,sprintf('%d_%d.bmp',nn,nni));
                if ~exist(patchnamepath,'file')
                    continue;
                end
                % loops over all patches that appear in V
                count1=count1+1;
                cla=idxk(count1,1);  % the cluster of the current patch
                posk=find(patchkernel==cla);  % patchkernel (cluster center patch) that represents this cluster
                kernelModel{viewi,1}(posk,nn)=kernelModel{viewi,1}(posk,nn)+1;
            end
        end
        fprintf('%d\n', viewi); 
    end

    KMname=fullfile(kernel_Path,'kernelModel.mat');
    save(KMname,'kernelModel');
    fprintf('finish run cluster idf\n');
end