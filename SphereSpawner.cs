using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class SphereSpawner : MonoBehaviour
{
    public GameObject spherePrefab;       // The sphere prefab to spawn
    public Slider spawnRateSlider;        // The UI slider to control spawn rate
    public Slider minSizeSlider;          // Slider for minimum sphere size
    public Slider maxSizeSlider;          // Slider for maximum sphere size
    public Slider minDistanceSlider;      // Slider for minimum spawn distance
    public Slider maxDistanceSlider;      // Slider for maximum spawn distance
    public Button toggleButton;           // The toggle button to start/stop spawning
    public float maxLifetime = 5f;        // Max lifetime of each sphere
    public int poolSize = 10000;          // Max number of spheres in the pool
    public AudioSource buttonAudioSource; // AudioSource for the button sound

    private GameObject[] spherePool;      // Pool to hold the spheres
    private int poolIndex = 0;            // Current index in the pool
    private bool isSpawning = false;      // To track if spawning is active

    private void Start()
    {
        // Initialize the pool of spheres
        spherePool = new GameObject[poolSize];
        for (int i = 0; i < poolSize; i++)
        {
            spherePool[i] = Instantiate(spherePrefab);
            spherePool[i].SetActive(false);  // Start with all spheres inactive
        }

        // Set slider defaults and ranges
        spawnRateSlider.maxValue = 10000;
        minSizeSlider.minValue = 0.1f;
        minSizeSlider.maxValue = 5f;
        maxSizeSlider.minValue = 0.1f;
        maxSizeSlider.maxValue = 5f;
        minDistanceSlider.minValue = 0f;
        minDistanceSlider.maxValue = 50f;
        maxDistanceSlider.minValue = 1f;
        maxDistanceSlider.maxValue = 50f;

        // Set up the button to toggle the spawning state
        toggleButton.onClick.AddListener(ToggleSpawning);
    }

    private void Update()
    {
        // Adjust spawn rate based on the slider value
        float spawnRate = spawnRateSlider.value;
        float spawnInterval = 1f / spawnRate;  // Time interval between spawns

        // Adjust sphere size and spawn distance based on sliders
        float minSize = minSizeSlider.value;
        float maxSize = maxSizeSlider.value;
        float minDistance = minDistanceSlider.value;
        float maxDistance = maxDistanceSlider.value;

        // Only spawn spheres if spawning is active
        if (isSpawning)
        {
            StartCoroutine(SpawnSpheres(spawnInterval, minSize, maxSize, minDistance, maxDistance));
        }
    }

    private IEnumerator SpawnSpheres(float spawnInterval, float minSize, float maxSize, float minDistance, float maxDistance)
    {
        while (isSpawning)
        {
            if (spawnRateSlider.value > 0)  // Only spawn if spawn rate is greater than 0
            {
                GameObject sphere = GetNextAvailableSphere();
                if (sphere != null)
                {
                    // Set a random position within the spawn radius
                    Vector3 randomPosition = Random.insideUnitSphere * Random.Range(minDistance, maxDistance);
                    sphere.transform.position = randomPosition;

                    // Set a random scale (size) for the sphere
                    float randomSize = Random.Range(minSize, maxSize);
                    sphere.transform.localScale = new Vector3(randomSize, randomSize, randomSize);

                    sphere.SetActive(true);

                    // Set a random lifetime for the sphere
                    float lifetime = Random.Range(1f, maxLifetime);
                    StartCoroutine(DeactivateAfterLifetime(sphere, lifetime));
                }
            }

            yield return new WaitForSeconds(spawnInterval);
        }
    }

    private GameObject GetNextAvailableSphere()
    {
        for (int i = 0; i < poolSize; i++)
        {
            poolIndex = (poolIndex + 1) % poolSize;
            if (!spherePool[poolIndex].activeInHierarchy)
            {
                return spherePool[poolIndex];
            }
        }
        return null;
    }

    private IEnumerator DeactivateAfterLifetime(GameObject sphere, float lifetime)
    {
        yield return new WaitForSeconds(lifetime);
        sphere.SetActive(false);
    }

    private void ToggleSpawning()
    {
        if (buttonAudioSource != null)
        {
            buttonAudioSource.Play();
        }

        isSpawning = !isSpawning;

        if (isSpawning)
        {
            toggleButton.GetComponentInChildren<Text>().text = "Stop Spawning";
        }
        else
        {
            toggleButton.GetComponentInChildren<Text>().text = "Start Spawning";
        }
    }
}
