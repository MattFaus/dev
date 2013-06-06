#!/bin/bash
if ls ~/.khantentTmp > /dev/null 2>&1
then
  rm ~/.khantentTmp
fi

echo "Welcome to Joshua Netterfield's super scary import script which acts as"
echo "proof that an import script can in fact be more hacky then Ben Komalo's"
echo
echo "This script will import an account from a Khan server. If it is missing"
echo "something that's critical to your work, ping me!"
echo
echo "You must be a Khan developer to use this script.. If you need to become"
echo "a developer on the site, ask one."
echo

read -p "Source (sans http://): [staging-dot-khan-academy.appspot.com] " REMOTE_SERVER
if [ "$REMOTE_SERVER" = "" ]; then
  REMOTE_SERVER="staging-dot-khan-academy.appspot.com"
fi;
echo $REMOTE_SERVER

echo
if [ ! -f ~/.khan-cookies_$REMOTE_SERVER ]; then
  echo "# First, download https://chrome.google.com/webstore/detail/cookietxt-export/lopabhfecdfhgogdbojmaicoicjekelh" >> ~/.khan-cookies_$REMOTE_SERVER
  echo "# Then, using Chrome, go to $REMOTE_SERVER, sign in as a dev and press the blue arrow button to the right of the URL bar" >> ~/.khan-cookies_$REMOTE_SERVER
  echo "# Copy everything from there into this file." >> ~/.khan-cookies_$REMOTE_SERVER

  echo I need cookies. See instructions in ~/.khan-cookies_$REMOTE_SERVER ...
  echo "Press ENTER once you've edited this file."
  read -p ""
else
  echo I found cookies, but if you need to change them, just edit ~/.khan-cookies_$REMOTE_SERVER
  echo
fi;

FKEY=$(cat ~/.khan-cookies_$REMOTE_SERVER | grep fkey | tail -n1 | sed 's/^.*fkey//' | sed 's/^[ \t]*//')

echo "Your fkey seems to be $FKEY (Press CTRL+C to abort if this is blank or incorrect)"
echo
read -p "Emails to import (space-seperated): " EMAIL
echo Going to import:
for v in $EMAIL
  do echo "    $v" | sed s/,//g
done
echo
read -p "Local server [0.0.0.0:8080]: " LOCAL_SERVER

if [ "$LOCAL_SERVER" = "" ]; then
  LOCAL_SERVER="0.0.0.0:8080"
fi;

echo
read -p "Press ENTER to start importing."

types=(UserData ProblemLog VideoLog UserBadge UserExercise UserTopic UserVideo VideoLog)

for v in $EMAIL
  do
    for i in "${types[@]}"
    do :
      echo Fetching entites of type $i for $(echo $v | sed s/,//g)...

      wget "http://$REMOTE_SERVER/api/v1/dev/protobuf-query/$i" --post-data="{\"max\": 10000, \"query\":[{\"key\": \"user\", \"operator\": \"=\", \"value\": \"USER($(echo $v | sed s/,//g ))\"}]}" --header="Content-Type: application/json" --header="x-ka-fkey: $FKEY" --load-cookies ~/.khan-cookies_$REMOTE_SERVER -O ~/.tmp/khantentTmp -nv
      if [ $PIPESTATUS -ne 0 ]; then
          echo "It's your fault. Got error from remote server. Run this script again, double checking all the parameters."
          exit
      fi

      while :; do

        wget "http://$LOCAL_SERVER/api/v1/dev/insert-protobuf/$i" --post-file="/home/joshua/.tmp/khantentTmp" --header="Content-Type: application/json" -O /dev/null -nv
        if [ $PIPESTATUS -ne 0 ]; then
            echo "It's your fault. The local server returned an error."
            echo "If you haven't done so already, you may need to patch the local server."
            echo "Patching it will make in insecure. If you're okay with that, enter the path to the webapp."
            echo "Once you're done with this script run 'git checkout -- api/v1_misc.py' to go back to normal."
            echo
            read -p "Path (or ENTER to try again, or CTRL+C to abort): " LOCALPATH
            if [ "$LOCALPATH" = "" ]; then
              continue
            fi
            echo "Waiting two seconds... (this may not be long enough)"
            sleep 2

            echo '

import pickle as pickleLib

@route("/api/v1/dev/insert-protobuf/<entity>", methods=["POST"])
@api.auth.decorators.open_access
def protobuf_inert(entity):
    # STOPSHIP(joshnetterfield): This code is not intended to be commited.
    payload = request.data;
    models = pickleLib.loads(payload)["result"];
    for m in models:
        print("Inserting model");
        model = db.model_from_protobuf(m);
        model.key()._Key__reference.app_ = "dev~khan-academy";
        model.put();
    return "Done";

' >> $LOCALPATH/api/v1_misc.py

        else
          break
        fi;
      done

      rm ~/.tmp/khantentTmp
  done
done

echo
echo "Data has been imported. Or maybe not. I didn't check."
echo "Log in as a user and see if you have data."
echo "Additionally, you should (as an admin) load $LOCAL_SERVER/admin/dailyactivitylog"
echo "so the pretty graphs load."
echo
echo "Also, don't forget to do 'git checkout -- api/v1_misc.py'..."