deploy:
	# Clean deployment folder
	rm -rf deployment
	mkdir deployment

	# Copy ansible playbook, python code and secrets
	cp -r ansible/* deployment
	cd python2 && cp -r * ../deployment/roles/provision/files/
	rm -rf deployment/roles/provision/files/tests
	rm -rf deployment/roles/provision/files/.gitkeep
	cp secrets.json deployment/secrets.json

	# Authenticate Onedrive and create refresh token session.pickle
	cp secrets.json deployment/roles/provision/files/energymeter/backup/secrets.json
	cd deployment/roles/provision/files/energymeter/backup && python3 setup_onedrive.py
	rm -rf deployment/roles/provision/files/energymeter/backup/setup_onedrive.py
	rm -rf deployment/roles/provision/files/energymeter/backup/secrets.json

	# Execute playbook
	cd deployment && ansible-playbook -i 192.168.168.128, -u pi --ask-pass --extra-vars "@secrets.json" site.yml
	#rm -rf deployment

test:
	cd python2 && python3 -m unittest discover -v

