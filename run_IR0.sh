# # #!/bin/sh


# Taking tags from the command line

while getopts f: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
    esac
done



# Checking if a file name is properly specified

if [ -z "$file" ]
    then
        echo "Please specify an object code"
        exit 1
fi



# Setting missing parameters if any

if [ -z "$target" ]
    then
        target="./tests"
        echo "test directory is set to './tests' "
fi

if [ -z "$size" ]
    then
        size=0
        echo "test size is set to 0 "
fi


# Copying a designated statement file

dir="/usr/src/app/"
orig="/code/"
cp $orig$file.py $dir$file.py


# Refresh the directory
rm -r irs
mkdir -p irs


# Actual Execution
echo "Running $file ....";

python3 $dir$file.py
dirlist=`ls irs`
echo $dirlist

# Creat dir
mkdir -p irs/wit
mkdir -p irs/ins

# Run firealarm test
cd irs && wtk-firealarm $dirlist && cd ..

echo "wtk-firealarm successfully completed"

# Copy into directory compatible with mac-and-cheese
for ir in ${dirlist}
    do
        if [[ "irs/$ir" == *.ins ]]
            then
                # if it has, move it to irs/ins
                mv ./irs/$ir ./irs/ins/$ir
        fi
        if [[ "irs/$ir" == *.wit ]]
            then
                # if it has, move it to irs/ins
                mv ./irs/$ir ./irs/wit/$ir
        fi
done
# copy the irs into local
cp -r ./irs /code