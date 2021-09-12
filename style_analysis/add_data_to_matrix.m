% add the all views' images feature into the matrix X
function []=add_data_to_matrix(lines_Path,kernel_Path,txt_Path,views,models,pslf_Path)
    fprintf('start add_data_to_matrix\n');
    if ~exist(pslf_Path,'dir')
        mkdir(pslf_Path);
    end
    %% add data into X
    X=cell(1,views);
    kk=0;
    for v=1:views
        % the names of images in this view
        allname=importdata(fullfile(txt_Path, sprintf('picname%d.txt',v)));
        % the names of patches representing clusters
        apidf=importdata(fullfile(kernel_Path,num2str(v),'Apidfpatchname.txt'));
        % each model is represented by 5*(num_clusters) values in one view
        % and these were created in "convolutional" step and are saved into
        % files. We read those files (A) and store them in V1
        rows=5*length(apidf);
        V1=zeros(rows,models);
        for i=1:size(V1,2)
            name=allname{i};
            fileID = fopen(fullfile(lines_Path,name),'r');
            formatSpec = '%f';
            A = fscanf(fileID,formatSpec);
            fclose(fileID);
            V1(:,i)=A;
        end
       kk=kk+1;
       % save the matrices of all views into X
       X{kk}=V1;
       fprintf('%d\n', v);
    end
   
    vname=fullfile(pslf_Path,'input.mat');
    save(vname,'X');
    fprintf('finish add_data_to_matrix\n');
end
